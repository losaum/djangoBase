from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from accounts.decorators import requer_perfil_ouro, requer_perfil_prata, requer_perfil_bronze


# @login_required
# def index(request):
#     return HttpResponse('<h1>Django</h1><p>Página simples.</p>')



def index(request):
    template_name = 'index.html'
    return render(request, template_name)

@login_required
def home(request):
    template_name = 'indexSigned.html'   
    return render(request, template_name)

@login_required
@requer_perfil_ouro(login_url="/")
def homeOuro(request):
    template_name = 'indexOuro.html'   
    return render(request, template_name) 

@login_required
@requer_perfil_prata(login_url="/")
def homePrata(request):
    template_name = 'indexPrata.html'   
    return render(request, template_name) 

@login_required
@requer_perfil_bronze(login_url="/")
def homeBronze(request):
    template_name = 'indexBronze.html'   
    return render(request, template_name) 

    