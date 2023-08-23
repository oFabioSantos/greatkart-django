from .models import *


def menu_links(request):
    """Esta função global está disponível a todos os templates sem passar por view.functions."""
    
    links = Category.objects.all()
    return dict(aurelio=links)  # links aqui é o nome de uma key que recebe links. Poderia ser qualquer nome. Esse obj tem acesso a função que tá no models
    