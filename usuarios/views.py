from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages, auth
from .forms import UsuarioLoginForm, UsuarioRegistrationForm, UsuarioEditForm
from vitrine_digital.helper import encriptarAESGCM, descriptarAESGCM
from .models import Usuario
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        else:
            return redirect('dashboard_usuario')
    data = {}
    data['form'] = UsuarioLoginForm()
    return render(request, 'login-usuario.html', data)

def valida_login(request):
    form = UsuarioLoginForm(request.POST or None)
    if form.is_valid():
        usuario = buscar_usuario_por_email(form.cleaned_data['email'])
        if usuario is None:
            messages.error(request, 'Usuário não encontrado')
        elif usuario.is_active is False:
            messages.error(request, 'O usuário foi desativado, entre em contato com o suporte')
        elif auth.authenticate(
            email = usuario.email,
            password = form.cleaned_data['password']
        ):
            auth.login(request, usuario)
            if usuario.is_superuser:
                return redirect('admin:index')
            else:
                return redirect('dashboard_usuario')
        else: 
            messages.error(request, 'Senha incorreta')
    return render(request, 'login-usuario.html', {'form': form})

def buscar_usuario_por_email(email: str, ativo: bool = False):
    usuarioEncontrado = None
    if ativo:
        usuarios = Usuario._default_manager.filter(**{
            'is_active': ativo
        })
    else:
        usuarios = Usuario.objects.all()
    for usuario in usuarios:
        if descriptarAESGCM(usuario.email).lower() == email.lower():
            usuarioEncontrado = usuario
            break
    
    return usuarioEncontrado

def cadastro(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        else:
            return redirect('dashboard_usuario')
    data = {}
    data['form'] = UsuarioRegistrationForm()
    return render(request, 'cadastro-usuario.html', data)

def valida_cadastro(request):
    form = UsuarioRegistrationForm(request.POST or None)
    if form.is_valid():
        usuario = Usuario.objects.create_user(
            email       =  encriptarAESGCM(form.cleaned_data['email']),
            password    =  form.cleaned_data['password'],
            first_name  =  encriptarAESGCM(form.cleaned_data['first_name']),
            last_name   =  encriptarAESGCM(form.cleaned_data['last_name']),
            cpf         =  encriptarAESGCM(form.cleaned_data['cpf'])
        )

        grupo = Group.objects.get(name='Usuário')

        usuario.groups.add(grupo)

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')
    
    return render(request, 'cadastro-usuario.html', {'form': form})

def retorna_empresas_favoritas_usuario(request):
    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'empresas-favoritas-usuario.html')#, data)

def retorna_meus_dados_usuario(request):
    data = {}

    usuario = get_object_or_404(Usuario, id=request.user.id)

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['imagem'] is not None and form.cleaned_data['imagem'] != '':
                usuario.imagem = form.cleaned_data['imagem']
            if form.cleaned_data['password'] is not None and form.cleaned_data['password'] != '':
                usuario.password = make_password(form.cleaned_data['password'])
                update_session_auth_hash(request, usuario)
            usuario.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('meus_dados_usuario')
    else:
        form = UsuarioEditForm(instance=usuario)

    data['form'] = form
    data['email'] = descriptarAESGCM(usuario.email)
    data['cpf'] = descriptarAESGCM(usuario.cpf)
    data['first_name'] = descriptarAESGCM(usuario.first_name)
    data['last_name'] = descriptarAESGCM(usuario.last_name)

    return render(request, 'meus-dados-usuario.html', data)

def retorna_produtos_salvos_usuario(request):
    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'produtos-salvos-usuario.html')#, data)

def retorna_pesquisar_empresas_usuario(request):
    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'pesquisar-empresas-usuario.html')#, data)