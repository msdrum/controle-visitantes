from django.shortcuts import render
from visitantes.models import Visitante

# Create your views here.
def index(request):

    todos_visitantes = Visitante.objects.all()

    context = {
        "nome_pagina": "Início da dashboard",
        "todos_visitantes": todos_visitantes,
    }

    return render(request, 'index.html', context)
