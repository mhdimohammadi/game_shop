from django.contrib import admin
from .models import Game



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title','price','genre']
    list_editable = ['price','genre']
    list_filter = ['created_at']
    search_fields = ['title','description']
    prepopulated_fields = {"slug": ("title",)}
