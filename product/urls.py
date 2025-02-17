from django.urls import path
from . import views


app_name = "game"
urlpatterns = [
   path("", views.index, name="index"),
   path('game_detail/<int:id>/',views.game_detail,name='game_detail'),
]
