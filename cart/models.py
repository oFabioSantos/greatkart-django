from django.db import models
from mysite.models import *

#  Cart models


class Cart(models.Model):
    """Representation of a shopping cart"""
    
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        """Text displayed at the admin panel"""
        
        return self.cart_id
    

class CartItem(models.Model):
    """Representation of itens from the shopping cart"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(ProductVariation, blank=True)  # Isso aqui vai conectar a classe produto
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity 
    
    def __str__(self):
        if self.product:
            return str(self.product)  # Se pá, o produto tá recebendo algum outro tipo de dados ao ser atrelado no car à session.
        else:
            None

# Em meu outro projeto, a estrutura estava parecida com esta, exceto que adicionei os dados de pagamento no carrinho, mas isso deve estar em uma classe dedicada.