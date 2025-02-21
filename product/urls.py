from django.urls import path
from . import views


app_name = "game"
urlpatterns = [
   path("", views.index, name="index"),
   path('game_detail/<int:id>/',views.game_detail,name='game_detail'),
   path('contact_us/',views.contact_us,name='contact_us'),
   path('games/',views.game_list,name='game_list'),
   path('games/<str:category>',views.game_list,name='games_by_category'),
]
