from django.shortcuts import render, get_object_or_404
from .models import Game


def index(request):
    games = Game.objects.all()
    best_offer = games.order_by('-off').first()
    trending_games = games.order_by('-created_at')[:4]
    most_played = games.order_by('-sold_count')[:6]
    context = {"best_offer":best_offer,"trending_games":trending_games,"most_played":most_played}
    return render(request, "../templates/product/index.html",context)


def game_detail(request, id):
    game = get_object_or_404(Game, id=id)
    similar_games = game.category.games.exclude(id=game.id)
    return render(request, "../templates/product/product-details.html", {"game": game, "similar_games": similar_games})




def contact_us(request):
    return render(request, "../templates/product/contact.html")