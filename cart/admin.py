from django.contrib import admin
from .models import *

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    """Customiza o painel de admin"""
    list_display = ('cart_id', 'created_at')
    

class CartItemAdmin(admin.ModelAdmin):
    """Customiza o painel de admin"""
    list_display = ('product', 'cart', 'quantity', 'is_active')    

admin.site.register(Cart, CartAdmin),
admin.site.register(CartItem, CartItemAdmin),


