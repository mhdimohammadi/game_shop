from django.contrib import admin
from .models import Game, Category, Ticket, CustomUser, Order, OrderItem
from .redis_utils import clear_game_cache

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title','price']
    list_editable = ['price']
    list_filter = ['created_at']
    search_fields = ['title','description']
    prepopulated_fields = {"slug": ("title",)}
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_game_cache(obj.id)








@admin.register(Category)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}




admin.site.register(Ticket)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderItem)