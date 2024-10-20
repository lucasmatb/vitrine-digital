from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.get(username=username)

        if user:
            return HttpResponse('Já existe um usuário com esse username')

        return HttpResponse(username)

def login(request):
    return render(request, 'login.html')

def figma(request):
    return render(request, 'figma.html')