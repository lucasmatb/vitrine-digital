from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages, auth
from .forms import UsuariosLoginForm, UsuariosRegistrationForm, trata_cpf_apenas_numeros
from vitrine_digital.helper import descriptarAESGCM
from .models import Usuarios

def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboards/index')
    data = {}
    data['form'] = UsuariosLoginForm()
    return render(request, 'login.html', data)

def valida_login(request):
    form = UsuariosLoginForm(request.POST or None)
    if form.is_valid():
        usuario = buscar_usuario_por_email(form.cleaned_data['email'])
        if usuario is None:
            messages.error(request, 'Usuário não encontrado')
        else:
            usuario = auth.authenticate(
                email = usuario.email,
                password = form.cleaned_data['password']
            )
            if usuario is not None:
                if usuario.is_active is False:
                    messages.error(request, 'O usuário foi desativado, entre em contato com o suporte')
                else:
                    print("Login deu certo")
                    auth.login(request, usuario)
                    if usuario.is_superuser:
                        return redirect('/admin')
                    else:
                        return redirect('/dashboards/index')
            else: 
                messages.error(request, 'Senha incorreta')

    return render(request, 'login.html', {'form': form})

def buscar_usuario_por_email(email: str):
    usuarioEncontrado = None
    usuarios = Usuarios.objects.all()
    for usuario in usuarios:
        if descriptarAESGCM(usuario.email).lower() == email.lower():
            usuarioEncontrado = usuario
            break
    
    return usuarioEncontrado

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
    
    return render(request, 'cadastro.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.error(request, 'Faça login antes de acessar a plataforma')
    return redirect('/auth/login/')
