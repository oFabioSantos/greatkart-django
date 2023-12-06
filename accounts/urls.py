# mysite url's

from django.urls import path
from .import views

app_name = 'accounts'
urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),   
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('renova_password/<uid64>/<token>/', views.renova_password, name='renova_password'),  # Tudo o que for enviado para o email do user, precisamos passar o tonek e o uid64
    path('reset_password/', views.reset_password, name='reset_password'),
]