# core url's
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mysite.urls')),
    path('cart/', include('cart.urls')),
    path('accounts/', include('accounts.urls'))
,] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #  Configuração para o Django servir arquivos estáticos no ambiente de desenvolvimento.
