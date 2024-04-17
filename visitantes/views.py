from django.shortcuts import render

# Create your views here.
def registrar_visitante(request):

    context = {}

    return render(request, "registrar_visitante.html", context)

