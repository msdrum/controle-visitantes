from django.shortcuts import (
    render, redirect, get_object_or_404
) 

from django.http import HttpResponseNotAllowed

from visitantes.forms import (
    VisitanteForm, AutorizaVisitanteForm
)
from django.contrib import messages
from visitantes.models import Visitante
from django.contrib.auth.decorators import login_required

from django.utils import timezone

# Create your views here.
@login_required
def registrar_visitante(request):

    form = VisitanteForm()

    if request.method == "POST":
        form = VisitanteForm(request.POST)

        if form.is_valid():
            visitante = form.save(commit=False)

            visitante.registrado_por = request.user.porteiro

            visitante.save()

            messages.success(
                request,
                "Visitante registrado com sucesso!"
            )

            return redirect("index")

    context = {
        "nome_pagina": "Registrar Visitante",
        "form": form
    }

    return render(request, "registrar_visitante.html", context)

@login_required
def informacoes_visitante(request, id):

    visitante = get_object_or_404(
        Visitante,
        id=id,
    )

    form = AutorizaVisitanteForm()

    if request.method == "POST":
        form = AutorizaVisitanteForm(
            request.POST,
            instance=visitante
        )

        if form.is_valid():
            visitante = form.save(commit=False)

            visitante.status = "EM_VISITA"
            visitante.horario_autorizacao = timezone.now()

            visitante.save()

            messages.success(
                request,
                "Entrada do visitante autorizada com sucesso!"
            )

            return redirect("index")

    context = {
        "nome_pagina": "Informações do visitante",
        "visitante": visitante,
        "form": form,
    }

    return render(request, "informacoes_visitante.html", context)

@login_required
def finalizar_visita(request, id):

    if request.method == "POST":
        visitante = get_object_or_404(
            Visitante,  # -> modelo do visitante
            id=id
        )

        visitante.status = "FINALIZADO" # -> muda o status da visita para finalizado
        visitante.horario_saida = timezone.now() # -> grava o horário exato da finalização

        visitante.save()

        messages.success(  # mostra a mensagem na tela do cliente
            request,
            "Visita finalizada com sucesso"
        )

        return redirect("index") # redireciona o usuário para a tela inicial
    else:
        return HttpResponseNotAllowed( # -> classe que vai bloquear o acesso por outros tipos de método
            ["POST"], # -> lista com os métodos que SERÃO PERMITIDOS!!!
            "Método não permitido"  # -> mensagem que será exibida, caso o usuário tente acessar a função através de um método não permitido.
        )