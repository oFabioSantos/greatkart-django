#  Cart views

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from mysite.models import *
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import *


def _cart_id(request):  #  Essa função cria um cart relacionado à session, retorna para a func add cart que relaciona um produto/cart item e quantidade.
    """Private function to be used only to get the session.id"""
    
    cart = request.session.session_key  # Get the data from the session_id
    if not cart:
        cart = request.session.create()  # Creates a session if not exists yet.
    return cart                      



def add_cart(request, product_id):  # Essa função recebe os dados da página detalhes do produto ao clicar em add to the cart.
    """Add a product in the cart, this is the main function"""
    
      
    # Isso aqui cria o carrinho
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Creates a cart instance with a session related.
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)  # Creates a car with a session related.
        )
    cart.save()  #  Aqui temos um cart object relacionado à sessão do usuário.   
    
    
    #  Isso aqui cata a variation
    product = Product.objects.get(id=product_id)  # Retreives the id product but I will use a slug later on.
    variation_product = []
    
    if request.method == "POST":  # Tem sempre que verificar o método dos dados que vieram do form.
        for x in request.POST:
            key = x  # recebe a parada do front, faz um select no banco e verifica se os valores são iguais aos selecinados no front. Aqui recebemos o índice.
            value = request.POST[key]  #  O value vai receber o valor presente no índice key. A var Key contém o key and value.
            print(key, value)
            
            try:
                variation = ProductVariation.objects.get(product=product, variation_choices__iexact=key, variation_values__iexact=value) # It ignores up and lower case
                variation_product.append(variation)  # Aqui tem uma lista com os produtos e auas variações.
            except:
                pass # Só vai catar produtos com variações exatas as que foram recebidas do front, caso contrário não fará nada.
                #  Até aqui entendi. Tenho que organizar melhor essa zona.
      
    
    #  Cart item
    cart_item_exists = CartItem.id #  Verifica se há itens no carrinho, mas devemos fazer isso verificando o id.
    if cart_item_exists: # Ele só pode criar um novo item se o produto não estiver no carrinho, dai temos que verificar. Caso esteja, deve incrementar a quantidade.
        cart_item = CartItem.objects.filter(product=product, cart=cart)  # The CartItem product field will receive the add_cart product value and the cart created.
        
        #  Precisamos de todas as variações do banco,
        #  Precisamos compara las com as do front
        
        ex_var_list = []
        id = []   
        for x in cart_item:
            variacoes_no_banco = x.variations.all()  # Cata todas as variações do banco.
            ex_var_list.append(list(variacoes_no_banco))  #  Monta uma lista com todas as variações
            id.append(x.id)  # A lista recebe o id de cada produto
            
        existing_variations_ids = [set(variation.id for variation in var_list) for var_list in ex_var_list]
        incoming_variation_ids = set(variation.id for variation in variation_product)    
        
        if incoming_variation_ids in existing_variations_ids:  #  Se a lista contendo as variações do front estiverem no banco, duas listas sendo comparadas podem apresentar b.o
            #  Incremeta a quantidade, e como são N cart_itens, precisamos de uma lista
            
           index =  existing_variations_ids.index(incoming_variation_ids)   
           item_id = id[index]            
           item = CartItem.objects.get(product=product, id=item_id)  #  O BO TÁ AQUI.
           item.quantity += 1  
           item.save()   
               
        else:
            #  Create a new cart_item              
            item = CartItem.objects.create(product=product, quantity = 1, cart=cart)
            if len(variation_product) > 0:
                item.variations.clear()  # É necessário limpar(esvaziar) o cart_item após salva lo para não haver redundância.
                item.variations.add(*variation_product)   
            item.save()
             
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,         
        )
        if len(variation_product) > 0:
            cart_item.variations.clear()  # Limpa as instâncias variations feitas anteriormente antes de adicionar e salvar, evitando duplicidade.
            cart_item.variations.add(*variation_product) 
        cart_item.save()             
    return redirect('cart:cart')  # Retorna à função cart que renderiza a página cart.html 


def remove_cart(request, product_id, cart_item_id):
    """Decreases the quantity of a product from the shopping cart"""
    
    product = get_object_or_404(Product, id=product_id)    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else: 
            cart = get_object_or_404(Cart, cart_id=_cart_id(request))  # Se tá chamando uma função, portanto há a necessidade do request. Quando o user é autenticado não precisa disso.  
            cart_items = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)  # Usuário não autenticado, chamamos cart que chama a create_cart que pega o user.        
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()  #  Se a quantidade for  = 1 e reduzirmos a quantidade, o ítem deverá ser excluído.
    except:
        pass        
    return redirect('cart:cart')


def remove_cart_item(request, product_id, cart_item_id):
    """Removes a product from the shopping cart"""
    
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
           cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
           cart = get_object_or_404(Cart, cart_id=_cart_id(request)) 
           cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    except:
        pass       
    cart_item.delete()
    
    return redirect('cart:cart')                
           

def cart(request, total=0, quantity=0, cart_items=None):  # Isso aqui é o reflexo do seu models.
    """Returns a shopping cart"""
    #  Isso aqui terá que retornar algo para o front
    #  Já tenho o produto e o carrinho salvos no banco, aqui farei o retreive dos dados
    grand_total = 0  # Se não houver objetos no carrinho, o block try não iniciará, por isso precisamos destas variáveis globais.
    tax = 0
    try:
        if request.user.is_authenticated:  # No usuário autenticado, usamos o filtro user instead of cart
           cart_items = CartItem.objects.filter(user = request.user, is_active=True) 
        else:   
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Aqui buscamos um carrinho que esteja relacionado à sessão atual, cookies.    
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)   # O carrinho foi criado com o id_session.
       
        for x in cart_items:  # One cart can have multiple products
            total += (x.product.price * x.quantity) 
            quantity += x.quantity  # On each loop, the quantity will be incremented by one.
        tax = (3 * total) / 100  # Nos eua, a alíquota é informada a parte do preço do produto.
        grand_total = total + tax
        
    except ObjectDoesNotExist: 
        pass #  Ignore for now             
                 
    context = {        
        "cart_items": cart_items,
        "quantity": quantity,
        "total": total,
        "tax": tax,
        "grand_total": grand_total,
               
    }    
    return render(request, 'mysite/cart.html', context)  # O cart só deve ser renderizado se houver algum produto nele.

