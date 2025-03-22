from django.contrib import admin
from .models import Game, Review, Category, Ticket, CustomUser, Order, OrderItem


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title','price']
    list_editable = ['price']
    list_filter = ['created_at']
    search_fields = ['title','description']
    prepopulated_fields = {"slug": ("title",)}



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author','game']
    list_filter = ['created_at']
    search_fields = ['game__title','author']



@admin.register(Category)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}




admin.site.register(Ticket)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderItem)