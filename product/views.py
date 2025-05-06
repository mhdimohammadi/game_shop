from urllib.parse import quote
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from .models import Game, Category, CustomUser, OrderItem
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from decouple import config
from .cart import Cart
import uuid
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def index(request):
    games = Game.objects.all()
    best_offer = games.order_by('-off').first()
    trending_games = games.order_by('-created_at')[:4]
    most_played = games.order_by('-sold_count')[:6]
    context = {"best_offer": best_offer, "trending_games": trending_games, "most_played": most_played}
    return render(request, "product/index.html", context)


def game_detail(request, id):
    cache_key = f'game_detail_{id}'
    game = cache.get(cache_key)
    if not game:
        game = get_object_or_404(Game, id=id)
        cache.set(cache_key, game, timeout=60 * 30)
    similar_games = Game.objects.filter(category_id=game.category).exclude(id=game.id)[:5]
    return render(request, "product/product-details.html", {"game": game, "similar_games": similar_games})


def contact_us(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket sent successfully!")
            return redirect('game:contact_us')
    else:
        form = TicketForm()
    return render(request, "product/contact.html", {"form": form})


@cache_page(60 * 30,key_prefix='game_list')
def game_list(request):
    games = Game.objects.all()
    categories = Category.objects.all()
    return render(request, "product/shop.html", {"games": games, "categories": categories})


def filter_games(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        games = Game.objects.all()
    else:
        games = Game.objects.filter(category__name=category)
    html = render_to_string('partials/game_list_items.html', {'games': games})
    return JsonResponse({'html': html})


def trending_game(request):
    games = Game.objects.all().order_by('-created_at')
    paginator = Paginator(games, 3)
    page_number = request.GET.get('page', 1)
    try:
        games = paginator.page(page_number)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        games = paginator.page(1)
    return render(request, 'product/trending.html', {'games': games})


def most_played_game(request):
    games = Game.objects.all().order_by('-sold_count')
    paginator = Paginator(games, 3)
    page_number = request.GET.get('page', 1)
    try:
        games = paginator.page(page_number)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        games = paginator.page(1)
    return render(request, 'product/most-played.html', {'games': games})


def user_login(request):
    cart_data = request.session.get('cart', {})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['cart'] = cart_data
                    messages.success(request, "You are now logged in!")
                    return redirect('game:index')
            else:
                messages.error(request, "Invalid username or password!")
                return redirect('game:login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='game:login')
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('game:index')


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"Welcome {user.username}!")
            return redirect('game:index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='game:login')
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('game:profile')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'product/profile.html', {'user': user, 'form': form})


def game_search(request):
    query = request.GET.get('query', None)
    games = []
    if query:
        games1 = Game.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gte=0.3)
        games2 = Game.objects.annotate(similarity=TrigramSimilarity('summary', query)).filter(similarity__gte=0.3)
        games = (games1 | games2).order_by('-similarity')
    return render(request, 'product/search.html', {'games': games, 'query': query})


serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


def generate_token(obj):
    return serializer.dumps({'obj': obj})


def verify_token(token):
    try:
        data = serializer.loads(token, max_age=600)
        return data['obj']
    except Exception:
        return None


@login_required(login_url='game:login')
def password_change(request):
    password = request.GET.get('password', None)
    user = request.user
    if password:
        if user.check_password(password):
            token = generate_token(user.id)
            token = quote(token)
            return redirect(f"{reverse('game:password_change_done')}?token={token}")
        else:
            messages.error(request, "Invalid password!")
            return redirect('game:password_change')

    return render(request, 'registration/password_change.html')


@login_required(login_url='game:login')
def password_change_done(request):
    token = request.GET.get('token')
    if not token or verify_token(token) != request.user.id:
        return HttpResponseForbidden("Invalid or expired token!")

    user = request.user
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, "Your password has been updated!")
            return redirect('game:profile')
    else:
        form = UserPasswordChangeForm()
    return render(request, 'registration/password_change_done.html', {'form': form})


def reset_password(request):
    email = request.GET.get('email', None)
    if email:
        if CustomUser.objects.filter(email=email).exists():
            unique_id = str(uuid.uuid4())
            token = serializer.dumps({'email': email, 'unique_id': unique_id}, salt='password-reset-salt')
            token = quote(token)
            html_content = render_to_string('email/reset_password_email.html', {
                'reset_url': f"http://127.0.0.1:8000{reverse('game:reset_password_done')}?token={token}"})
            email_message = EmailMultiAlternatives(
                'reset password',
                "If you’re trying to reset your password, use the link provided in the email.",
                config("EMAIL_HOST_USER"),
                [email],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()
            messages.success(request, "Email has been sent!")
            return redirect('game:login')
        else:
            messages.error(request, "Invalid email!")
            return redirect('game:reset_password')

    return render(request, 'registration/reset_password.html')


def reset_password_done(request):
    token = request.GET.get('token')
    try:
        date = serializer.loads(token, salt='password-reset-salt')
        email = date['email']
        user = CustomUser.objects.get(email=email)
    except (BadSignature, SignatureExpired):
        return HttpResponseForbidden("Invalid token!")
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, "Your password has been updated!")
            return redirect('game:login')
    else:
        form = UserPasswordChangeForm()
    return render(request, 'registration/reset_password_done.html', {'form': form, 'user': user})


@require_POST
def add_to_cart(request, game_id):
    try:
        cart = Cart(request)
        game = get_object_or_404(Game, id=game_id)
        cart.add_to_cart(game)
        context = {"sus": "Game has been added to your cart"}
        return JsonResponse(context)
    except:
        return JsonResponse({'error': 'invalid request'})


def cart_printer(request):
    cart = Cart(request)
    print(cart.cart)
    return HttpResponse(f"{cart}")


@require_POST
def update_quantity(request):
    game_id = request.POST.get('game_id')
    action = request.POST.get('action')
    try:
        game = get_object_or_404(Game, id=game_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(game)
        elif action == 'decrease':
            cart.decrease(game)
        context = {
            'total_price': cart.total_price(),
            'quantity': cart.cart[game_id]['quantity'],
            'game_total_price': cart.cart[game_id]['quantity'] * cart.cart[game_id]['price'],
            'success': True,
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success': False, 'error': 'item not found'})


@require_POST
def remove_game(request):
    game_id = request.POST.get('game-id')
    try:
        game = get_object_or_404(Game, id=game_id)
        cart = Cart(request)
        cart.remove(game)
        context = {
            'total_price': cart.total_price(),
            'success': True,
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success': False, "error": 'Item NOt Found'})


@login_required(login_url='game:login')
def picture_change(request):
    if request.method == 'POST':
        user = request.user
        if 'image' in request.FILES:
            user.image = request.FILES['image']
            user.save()
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.error(request, 'No image selected.')
        return redirect('game:profile')


@login_required(login_url='game:login')
def order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            _order = form.save(commit=False)
            _order.buyer = request.user
            _order.paid = True
            _order.save()
            for item in cart:
                OrderItem.objects.create(order=_order, game=item['game'], quantity=item['quantity'])
            cart.clear()
            messages.success(request, 'Order has been created successfully!')
            return redirect('game:index')
    else:
        form = OrderForm()
    return render(request, 'product/order.html', {'form': form})
