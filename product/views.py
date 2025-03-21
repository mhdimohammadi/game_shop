from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Category
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import TicketForm, LoginForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout


def index(request):
    games = Game.objects.all()
    best_offer = games.order_by('-off').first()
    trending_games = games.order_by('-created_at')[:4]
    most_played = games.order_by('-sold_count')[:6]
    context = {"best_offer": best_offer, "trending_games": trending_games, "most_played": most_played}
    return render(request, "product/index.html", context)


def game_detail(request, id):
    game = get_object_or_404(Game, id=id)
    similar_games = game.category.games.exclude(id=game.id)
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


def game_list(request):
    games = Game.objects.all()
    categories = Category.objects.all()
    return render(request, "product/shop.html", {"games": games, "categories": categories})


def filter_games(request):
    # Retrieve category from query parameters; default to "all"
    category = request.GET.get('category', 'all')

    # Filter games based on category
    if category == 'all':
        games = Game.objects.all()
    else:
        # Adjust the lookup according to your Game model relationships/fields
        games = Game.objects.filter(category__name=category)

    # Render a partial template with the filtered games
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
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You are now logged in!")
                    return redirect('game:index')
            else:
                messages.error(request, "Invalid username or password!")
                return redirect('game:login')
    else:
       form = LoginForm()
    return render(request,'registration/login.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('game:index')