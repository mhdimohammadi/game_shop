from django.urls import path
from . import views


app_name = "game"
urlpatterns = [
   path("", views.index, name="index"),
   path('game_detail/<int:id>/',views.game_detail,name='game_detail'),
   path('contact_us/',views.contact_us,name='contact_us'),
   path('games/', views.game_list, name='game-list'),
   path('filter_games/', views.filter_games, name='filter_games'),
   path('trending_games/', views.trending_game, name='trending_games'),
   path('most_played/', views.most_played_game, name='most_played'),
   path('login/', views.user_login, name='login'),
   path('logout/', views.user_logout, name='logout'),
]
