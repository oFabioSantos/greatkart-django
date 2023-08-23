from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Representation of the category of a product"""
    
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    categ_image = models.ImageField(upload_to='images/', null=True, blank=True)   
               
        
    def get_url(self):
        """Disponibiliza o Slug para o context processor."""
        
        return reverse('mysite:products_by_category', args=[self.slug])  # Para retornar um atributo de uma classe, usa-se o self. Products_by....é o nome da rota           
    
    
    class Meta:
        ordering = ('category_name',)
        verbose_name_plural = 'Categories'   
                    

    def __str__(self):
        return self.category_name    
   
    
    
    
class Product(models.Model):
    """Representation of a product"""  
    
    STATUS_CHOICES = (
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ) 
    
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Ativo')
    images = models.ImageField(upload_to='images/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE) 
    
    
    def get_url(self):
        """Retorna o slug do produto"""
        
        return reverse('mysite:product_detail', args=[self.category.slug, self.slug]) #  Isso aqui disponibilizará as slugs de categoria e produto a todos os templates.
    
    
    class Meta:
        ordering = ('product_name',)
        verbose_name_plural = 'Products'
        
    def __str__(self):
        return self.product_name    