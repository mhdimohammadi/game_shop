from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from .models import Game




def game_detail(request,id):
    game = get_object_or_404(Game,id=id)
    genres = game.genres
    # Construct a Q object for each genre
    genre_queries = Q()
    for genre in genres:
        genre_queries |= Q(genres__contains=genre)
    similar_games = Game.objects.filter(genre_queries).exclude(id=game.id).distinct()
    return render(request,"../templates/product/product-details.html",{"game":game,"similar_games":similar_games})