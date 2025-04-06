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
   path('register/', views.user_register, name='register'),
   path('profile/', views.profile, name='profile'),
   path('search/', views.game_search, name='search'),
   path('password_change', views.password_change, name='password_change'),
   path('password_change_done', views.password_change_done, name='password_change_done'),
   path('reset_password', views.reset_password, name='reset_password'),
   path('reset_password_done', views.reset_password_done, name='reset_password_done'),
   path('add_to_cart/<int:game_id>/', views.add_to_cart, name="add_to_cart"),
   path('cart/', views.cart_printer, name="cart"),
   path('update_quantity/', views.update_quantity, name="update_quantity"),
   path('remove_game/', views.remove_game, name="remove_game"),
   path('picture_change/', views.picture_change, name="picture_change"),
   path('order/', views.order, name="order"),
]
