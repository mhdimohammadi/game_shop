from django.contrib import admin
from .models import Game,Review



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title','price','genres']
    list_editable = ['price','genres']
    list_filter = ['created_at']
    search_fields = ['title','description']
    prepopulated_fields = {"slug": ("title",)}



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author','game']
    list_filter = ['created_at']
    search_fields = ['game__title','author']