from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Criaremos um custom template de autenticação

class MyAccountManager(BaseUserManager):
    """Pega as informações do template criado em account e criar as diretrizes de usuário e super usuário"""
    
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
       
        if not username:
            raise ValueError('User must have an username')
        
        #  Isso aqui cria um instância/objeto da classe Account
        user = self.model(
           email = self.normalize_email(email),
           username = username,
           first_name = first_name, 
           last_name = last_name,
        )
    
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        """Cria um usuário com a função anterior e atribui os privilégios."""
        
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        
        # Configuração dos privilégios de usuário
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user
        


class Account(AbstractBaseUser):
    """Template para o sistema custom de autenticação"""
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    
    
    #  Campos obrigatórios para um usuário autenticado    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    
    
    #  Isso aqui deve estar separado no próximo projeto FN2 (Perfil de Usuário)    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # Isso aqui diz ao Django sobreescrever o auth padrão por nosso custom manager.
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    #  Verifica se o usuário é um admin
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Permite que se o user for admin, terá acesso a todos os módulos. Add label é uma função built-in que garante permissões ao usuário se função anterior for True.
    def has_module_perms(self, add_label):
        return True