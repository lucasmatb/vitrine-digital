from django.contrib.messages import constants
from django.shortcuts import render
from django.shortcuts import redirect
from hashlib import sha256
from django.contrib import messages, auth
from .models import Usuarios

def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboards/index')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/dashboards/index')
    status = request.GET.get('status')
    return  render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    first_name = request.POST.get('primeiro_nome')
    last_name = request.POST.get('sobrenome')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    if len(first_name.strip()) == 0 or len(last_name.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Os campos não podem ficar vazios')
        return redirect('/auth/cadastro/')

    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'Sua senha deve ter no mínimo 8 caracteres')
        return redirect('/auth/cadastro/')
    #falta validação cpf
    if Usuarios.objects.filter(email = email).exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse email')
        return redirect('/auth/cadastro/')

    try:
        usuario = Usuarios.objects.create_user(
            email = email,
            password = senha,
            first_name = first_name,
            last_name = last_name
        )
        usuario.save()

        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
        return redirect('/auth/cadastro/')

    except:
        messages.add_message(request, constants.ERROR, 'Erro no cadastro de usuário')
        return redirect('/auth/cadastro/')

def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    usuario = auth.authenticate(email = email, password = senha)

    if not usuario:
        messages.add_message(request, constants.WARNING, 'Email ou senha inválido')
        return redirect('/auth/login/')    
    else:
        auth.login(request, usuario)
        return redirect('/dashboards/index')

def logout(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar a plataforma')
    return redirect('/auth/login/')