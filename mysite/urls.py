# mysite url's

from django.urls import path
from .import views

app_name = 'mysite'
urlpatterns = [
    
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),  # Duas urls para uma mesma função...
    path('store/<slug:category_slug>/', views.store, name='products_by_category'),  # Apontam para a mesma view porém referencia o método da classe model Category.
    path('product_detail/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
    
]