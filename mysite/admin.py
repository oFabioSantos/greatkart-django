from django.contrib import admin
from .models import *

# Aqui podemos sobreescrever o funcionamento padrão do painel Django.


class CategoryAdmin(admin.ModelAdmin):
    """Customização e geração automática do slug"""
    
    prepopulated_fields = {'slug': ('category_name',)}  # O slug receberá o content category_name de forma automática e formatada adequadamente.
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)



class ProductAdmin(admin.ModelAdmin):
    """Preenchimento automático da slug"""
    
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'stock', 'status', 'category', 'modified_date')

admin.site.register(Product, ProductAdmin)


