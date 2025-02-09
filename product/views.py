from django.shortcuts import render
from .models import Game




def game_detail(request,id):
    game = Game.objects.get(id=id)
    return render(request,"../templates/product/product-details.html",{"game":game})