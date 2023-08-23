from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

#  Isso aqui faz o override da visualização padrão do Django.
class AccountAdmin(UserAdmin):
    """Permite criar uma visualização customizada no painel admin."""
    
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')  # Nomes clicáveis.
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    
    #  Campos necessários para exibir um custom admin pannel quando usamos o custom auth.
    filter_horizontal = ()
    list_filter = ()
    fieldsets = () 



admin.site.register(Account, AccountAdmin)
