from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages, auth
from .forms import UsuariosLoginForm, UsuariosRegistrationForm, trata_cpf_apenas_numeros
from .models import Usuarios
import re

def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboards/index')
    data = {}
    data['form'] = UsuariosLoginForm()
    return render(request, 'login.html', data)

def valida_login(request):
    form = UsuariosLoginForm(request.POST or None)
    if form.is_valid():
        usuario = auth.authenticate(
            email = form.email,
            password = form.senha
        )
        auth.login(request, usuario)
        return redirect('/dashboards/index')
    else:
        messages.error(request, 'Email ou senha inválido')
        return redirect('/auth/login/')

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/dashboards/index')
    data = {}
    data['form'] = UsuariosRegistrationForm()
    return render(request, 'cadastro.html', data)

def valida_cadastro(request):
    form = UsuariosRegistrationForm(request.POST or None)
    if form.is_valid():
        cpfTratado = trata_cpf_apenas_numeros(form.cleaned_data['cpf'])

        Usuarios.objects.create_user(
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            cpf = cpfTratado
        )

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('/auth/login/')
    else:
        pass
    
    return render(request, 'cadastro.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.error(request, 'Faça login antes de acessar a plataforma')
    return redirect('/auth/login/')
