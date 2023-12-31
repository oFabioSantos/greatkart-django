#  Cart

from .views import *
from .views import _cart_id


def cart_icon(request):
    """Retorna a quantidade de itens no carrinho para aparecer naquele item."""
    
    itens = 0
    try:  # Se o cart existir
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Recupera o carrinho atrelado à sessão atual.
        if request.user.is_authenticated:
           cart_items = CartItem.objects.filter(user=request.user) #  Agora os cart_itens são relacionados ao usuário.
        else:   
            cart_items = CartItem.objects.all().filter(cart=cart)  #  Ele precisa saber qual carrinho chamar. 
        for x in cart_items:       
            itens += x.quantity
    except Cart.DoesNotExist:
        pass        
    return dict(quantidade=itens)  # Novamente, o car_item não existe sem o cart e os produtos.