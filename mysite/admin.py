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
    
    
class VariationAdmin(admin.ModelAdmin):
    """Personaliza a exibição das variações no painel"""  
    
    list_display = ('product', 'variation_choices', 'variation_values', 'status')
    list_editable = ('status',)  #  Tuplas devem conter uma vírgula no final.

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariation, VariationAdmin)   


