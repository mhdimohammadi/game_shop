from django.urls import path
from . import views


app_name = "product"
urlpatterns = [
   path('game_detail/<int:id>/',views.game_detail,name='product_detail'),
]
