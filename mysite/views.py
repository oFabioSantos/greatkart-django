from django.shortcuts import render, get_object_or_404

from cart.views import _cart_id  # Uma função privada deve ser importada da maneira descritiva, mas isso é uma má prática, tal função não deve ser utilizada across the app.
from .models import *

from cart.models import *
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


# Create your views here.


def index(request):
    """Returns the main page of the app"""
    
    products = Product.objects.all().filter(status='Ativo')  # products = Product.objects.filter(status='Ativo') performs better and its more concise.
    context = {
        'products': products
    }        
    return render(request, 'mysite/index.html', context)



def store(request, category_slug=None):  #  A função recebe um parâmetro opcional, por isso o slug recebe o padrão = None
    """Returns the store page and products"""
    
    products_count = 0
    products = None  # Variáveis inicializadas para serem reconhecidas dentro e fora do loop.
    categories = None   
    
    if category_slug != None:
       #  Se a slug não for vazia, retorna os produtos relacionados a ela. 
       
       categories = get_object_or_404(Category, slug=category_slug)  # Busca a categoria passada por parâmetro.
       products = Product.objects.filter(category=categories, status='Ativo')  #  Retorna o produto da categoria passada. 
       paginator = Paginator(products, 6)
       page = request.GET.get('page')
       paged_products = paginator.get_page(page)
       products_count = products.count()              
    
    else:
        products = Product.objects.filter(status='Ativo')
        paginator = Paginator(products, 6) # Número de produtos que desejamos imprimir por página. Quebra a queryset em pedaços, neste caso 6.
        page = request.GET.get('page')  # Isso aqui pega o índice da página da url, quando usamos o paginator, cada url ganha uma key 'page': x=numero da página.
        paged_products = paginator.get_page(page)  # Isso aqui retorna um número de índice válido para ser trabalhado no template, caso contrário retorna a página principal.
        products_count = products.count()  
        
        #categories = Category.objects.all()  # Tente usar o select related.....              
        
    context = {
        'paged_products': paged_products,
        'categories': categories,
        'product_count': products_count,      
    }                
    return render(request, 'mysite/store.html', context)


def product_detail(request, category_slug, product_slug):
    """Retorna o template de detalhe dos produtos"""
    
    try:        
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug, status='Ativo')  # obtemos a slug da categoria via fk e o slug do produto com a query.
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()  # Isso é uma má prática, seria melhor quebrar a FN e flagear o produto.
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,            
    }  #  Tá, mas na próxima, remova essa bagaça aqui, nada de usar uma função privada em outra função/módulo, isso é uma baita de uma gambiarra.    
    
    return render(request, 'mysite/product_detail.html', context)


def search_product(request):
    """Possibilita a busca de produtos"""
    
    
    paged_products = None
    products_count = None
    
    if 'keyword' in request.GET:    
        search = request.GET['keyword']  # Pega o conteúdo direto do form se houver algo digitado.
        
        if search:  # Verifica se o conteúdo é válido            
           paged_products = Product.objects.filter(Q(product_name__icontains=search) | Q(description__icontains=search))
           products_count = paged_products.count()   
        else:
            products_count = 0                    
               
    context = {
        'paged_products': paged_products, 
        'product_count': products_count,    #  Cuidado com os nomes das variáveis do context se este for utilizado por multiplas views.   
    }
    
    return render(request, 'mysite/store.html', context)

    


