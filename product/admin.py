from django.contrib import admin
from .models import Game, Category, Ticket, CustomUser, Order, OrderItem


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title','price']
    list_editable = ['price']
    list_filter = ['created_at']
    search_fields = ['title','summary']
    prepopulated_fields = {"slug": ("title",)}









@admin.register(Category)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}




admin.site.register(Ticket)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderItem)