from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.


def index(request):
    """Returns the main page of the app"""
    
    products = Product.objects.all().filter(status='Ativo')
    context = {
        'products': products
    }        
    return render(request, 'mysite/index.html', context)



def store(request, category_slug=None):  #  A função recebe um parâmetro opcional, por isso o slug recebe o padrão = None
    """Returns the store page and products"""
    
    products = None  # Variáveis inicializadas para serem reconhecidas dentro e fora do loop.
    categories = None   
    
    if category_slug != None:
       #  Se a slug não for vazia, retorna os produtos relacionados a ela. 
       
       categories = get_object_or_404(Category, slug=category_slug)  # Busca a categoria passada por parâmetro.
       products = Product.objects.filter(category=categories, status='Ativo')  #  Retorna o produto da categoria passada.             
    
    else:
        products = Product.objects.all().filter(status='Ativo')
        #categories = Category.objects.all()  # Tente usar o select related.....              
        
    context = {
        'products': products,
        'categories': categories,      
    }                
    return render(request, 'mysite/store.html', context)


def product_detail(request, category_slug, product_slug):
    """Retorna o template de detalhe dos produtos"""
    
    try:        
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug, status='Ativo')  # obtemos a slug da categoria via fk e o slug do produto com a query.
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,            
    }    
    
    return render(request, 'mysite/product_detail.html', context)


