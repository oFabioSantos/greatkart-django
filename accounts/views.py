from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from .forms import RegistrationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from cart.models import *
from cart.views import _cart_id
from mysite.models import *

# Email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage




# Create your views here.

def register(request):
    
    if request.method != 'POST':
       form = RegistrationForm()  # Cria uma instância vazia do post
    else:
        form = RegistrationForm(request.POST)  # Recebe um dicionário com toda parada do front
        if form.is_valid():
            # O clean() roda aqui, antes dos dados serem salvos
            first_name = form.cleaned_data['first_name']  #  o form recebe a função cleaned_data que criamos e recebe o método clean() Isso é essencial para autenticações.
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number'] 
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']  # Isso aqui pega toda a parada do front para ser validada no banco.
            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number= phone_number
            try:
                user.save() 
                
                # User activation 
                current_site =  get_current_site(request)   # Obtem o atual domínio da aplicação.
                email_subject = 'Please activate your account'  #  Descreve o título do email a ser enviado.
                message =  render_to_string('accounts/activate.html',{  # Conteúdo do corpo da mensagem enviada.
                    'user':user,
                    'domain': current_site, # Local onde a app está instalada, no momento está em localhost.
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    
                })  
                
                to_email = email
                send_email = EmailMessage(email_subject, message, to=[to_email])  # Monta um email com as informações coletadas
                send_email.send()  #  Envia o email
                
                
                messages.success(request, 'Register almost done, please check your email to finish you registration.')
                return HttpResponseRedirect(reverse('accounts:login_view'))
            except:
                messages.error(request, 'Error, something went wrong, please try again')    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.method != "POST":           
       return render(request, 'accounts/login.html')
    else:
       email = request.POST["Email Address"]
       password = request.POST["Password"]
       
       user = auth.authenticate(email=email, password=password) # Valida as informações no banco
       if user is not None:  # Se o user estiver autenticado
           try:
               print('entrando no bloco')  # teste para saber até onde o trecho do código está sendo executado.
               cart = Cart.objects.get(cart_id=_cart_id(request))  #  Se o user não for vazio, vou chamar a view function _cart_id para criar um carrinho
               is_cart_item_exists = CartItem.objects.filter(cart=cart).exists() #  Vai catar o session_id do browser e adicionar ao carrinho, ainda sem user autenticado.
               if is_cart_item_exists:
                   cart_item = CartItem.objects.filter(cart=cart)   # Relaciona o cart_item ao cart
                   
                   for x in cart_item:  #  O cart item deve conter um user id para o caso do cliente não estar logado?
                       x.user = user
                       x.save()
                   
           except:  
               print('entrando no block except')                                              
               pass
           auth.login(request, user)  # auth.login é uma função robusta, responsável por montar a sessão do usuário com as infos obtidas no user.
           messages.success(request, 'You are logged in.')
           return HttpResponseRedirect(reverse('cart:cart'))  # Ou (reverse('mysite:checkout'))  
       else:
           messages.error(request, 'Invalid credentials. Please try again.')
          # return render(request, 'accounts/login.html')         
       
@login_required(login_url= 'accounts:login_view')  # aqui consigo dizer para onde ele será redirecionado caso não esteja logado       
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mysite:index'))


def activate(request, uidb64, token):
    """Activate the user throught the email link received"""
    
    #  Tem que fazer o decode da parada que vem do email
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # após o decode, nos dará a primary key do user.
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None        
        #  return HttpResponse("user ativado")  Isso aqui serve para testar o endpoint
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Registration completed.')
        return HttpResponseRedirect(reverse('accounts:login_view'))
    else:
        messages.error(request, 'Something went wrong. Please try again.') 
        return redirect('accounts:register')   
        
@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgot_password(request):  #  Estude essa lógica aqui Fábio. Tá, essa função representa a lógica de enviar o email para o user.
    if request.method != 'POST':
       return render(request, 'accounts/forgot_password.html') # O uid realiza o encode e decode da pk, necessária para linkar o user à função.
    else:
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():  # Verifica se o email vindo do front está contido no campo email do db.
           user = Account.objects.get(email__exact=email)  # O filtro exact verifica se o dados são exatamente iguais, isso é importante na validação.
           
           current_site =  get_current_site(request)   # Obtem o atual domínio da aplicação.
           email_subject = 'Please reset your password'  #  Descreve o título do email a ser enviado.           
           message =  render_to_string('accounts/reset_password.html',{  # Conteúdo do corpo da mensagem enviada.
                
                'user':user,
                'domain': current_site, # Local onde a app está instalada, no momento está em localhost.
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)            
            }),                    
            
                
           to_email = email
           send_email = EmailMessage(email_subject, message, to=[to_email])  # Monta um email com as informações coletadas
           send_email.send()
           return HttpResponseRedirect(reverse('accounts:login_view'))
            
        else:
            messages.error(request, 'Account does not exist')  # Só é possível recuperar uma conta se ela existe.
            return HttpResponseRedirect(reverse('accounts:forgot_password'))
        

def renova_password(request,  uidb64, token):  # Essa view é para enviar o email redirecioando para a função reset password.
     """Allows user to reset its password"""      
     try:
        uid = urlsafe_base64_decode(uidb64).decode()  # após o decode, nos dará a primary key do user.
        user = Account._default_manager.get(pk=uid)
     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None    
     
     if user is not None and default_token_generator.check_token(user, token):
         request.session['uid'] = uid
         messages.success(request, 'Please reset your password')
         return redirect('accounts:reset_password')
     else:
         messages.error(request, 'This link has been expired!')
         return HttpResponseRedirect(reverse('accounts:login_view'))
         

def reset_password(request):
    if request.method == "POST":
       password = request.POST['password']
       confirm_password = request.POST['confirm_password']
       
       if password == confirm_password:
          uid = request.session.get('uid')
          user = Account.objects.get(pk=uid)
          user.set_password(password) # Usamos a função set_password e não a .save() pois assim ele será salvo em rash.
          user.save()
          messages.success(request,'Password reset successfully.')
          return redirect('accounts:login_view')
       else:
           messages.error(request,'Passwords do not match!')    
           return redirect('accounts:reset_password')    
    else:      
        return render(request, 'accounts/reset_password.html')   