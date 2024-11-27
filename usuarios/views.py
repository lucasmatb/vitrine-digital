from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages, auth
from .forms import UsuarioLoginForm, UsuarioRegistrationForm, trata_cpf_apenas_numeros
from vitrine_digital.helper import encriptarAESGCM, descriptarAESGCM
from .models import Usuario
from django.contrib.auth.models import Group

def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        else:
            return redirect('home-area-cliente')
    data = {}
    data['form'] = UsuarioLoginForm()
    return render(request, 'login-usuario.html', data)

def valida_login(request):
    form = UsuarioLoginForm(request.POST or None)
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
                    auth.login(request, usuario)
                    if usuario.is_superuser:
                        return redirect('admin:index')
                    else:
                        return redirect('home-area-cliente')
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
            return redirect('home-area-cliente')
    data = {}
    data['form'] = UsuarioRegistrationForm()
    return render(request, 'cadastro-usuario.html', data)

def valida_cadastro(request):
    form = UsuarioRegistrationForm(request.POST or None)
    if form.is_valid():
        cpfTratado = trata_cpf_apenas_numeros(form.cleaned_data['cpf'])

        usuario = Usuario.objects.create_user(
            email = encriptarAESGCM(form.cleaned_data['email']),
            password =  form.cleaned_data['password'],
            first_name =  encriptarAESGCM(form.cleaned_data['first_name']),
            last_name =  encriptarAESGCM(form.cleaned_data['last_name']),
            cpf =  encriptarAESGCM(cpfTratado)
        )

        grupo = Group.objects.get(name='Usuário')

        usuario.groups.add(grupo)

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('/auth/login/')
    
    return render(request, 'cadastro-usuario.html', {'form': form})