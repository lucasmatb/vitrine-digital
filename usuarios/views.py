from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages, auth
from .forms import UsuarioLoginForm, UsuarioRegistrationForm, UsuarioEditForm
from vitrine_digital.helper import encriptarAESGCM, descriptarAESGCM
from .models import Usuario, Pedido_Lojista
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from empresas.models import Cidade
from django.db.models import Count
from produtos.models import Imagem_Produto
from django.conf import settings
from django.core.paginator import Paginator

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
            cpf         =  encriptarAESGCM(form.cleaned_data['cpf']),
            nascimento  =  encriptarAESGCM(str(form.cleaned_data['nascimento'])),
        )

        grupo = Group.objects.get(name='Usuário')

        usuario.groups.add(grupo)

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')
    
    return render(request, 'cadastro-usuario.html', {'form': form})

def retorna_empresas_favoritas_usuario(request):
    data = {}
    
    empresas = request.user.favorito_empresa.all().annotate(
        favoritos=Count('favoritos_empresas')
    )

    empresas_com_favoritos = [
        {
            'id': empresa.id,
            'nome_fantasia': empresa.nome_fantasia,
            'descricao': empresa.descricao,
            'imagem_perfil': empresa.imagem_perfil,
            'imagem_capa': empresa.imagem_capa,
            'categorias': empresa.empresa_categoria.all(),
            'favorito_usuario': empresa.favoritos_empresas.filter(id=request.user.id).exists(),
            'favoritos': empresa.favoritos
        }
        for empresa in empresas
    ]

    paginator = Paginator(empresas_com_favoritos, 5)
    pages = request.GET.get('page')

    data['empresas'] = paginator.get_page(pages)

    return render(request, 'empresas-favoritas-usuario.html', data)

def retorna_meus_dados_usuario(request):
    data = {}

    usuario = get_object_or_404(Usuario, id=request.user.id)

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, request.FILES or None)
        estado = request.POST.get("estado")
        if estado:
            form.fields["cidade"].queryset = Cidade.objects.filter(id_estado=estado)
        if form.is_valid():
            if form.cleaned_data['imagem'] is not None and form.cleaned_data['imagem'] != '':
                usuario.imagem = form.cleaned_data['imagem']
            if form.cleaned_data['password'] is not None and form.cleaned_data['password'] != '':
                usuario.password = make_password(form.cleaned_data['password'])
                update_session_auth_hash(request, usuario)
            if form.cleaned_data['cidade'] is not None and form.cleaned_data['cidade'] != '':
                usuario.id_cidade = Cidade.objects.filter(id_estado=estado, pk=form.cleaned_data['cidade'].id).first()
            else:
                usuario.id_cidade = None
            usuario.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('meus_dados_usuario')
    else:
        form = UsuarioEditForm(instance=usuario)

    if usuario.id_cidade is not None:
        form.fields['cidade'].queryset = Cidade.objects.filter(id_estado=usuario.id_cidade.id_estado)
        data['cidade_selecionada'] = usuario.id_cidade.id
        data['estado_selecionado'] = usuario.id_cidade.id_estado.id
    else:
        data['cidade_selecionada'] = None
        data['estado_selecionado'] = None

    if request.user.has_perm('empresas.add_empresa'):
        usuario_tem_pedido_em_aguardo = 'lojista'
    elif Pedido_Lojista.objects.filter(
            id_usuario=request.user,
            status_pedido='Aguardando avaliação'
        ).exists():

        usuario_tem_pedido_em_aguardo = 'aguardando'
    else:
        usuario_tem_pedido_em_aguardo = 'usuario'

    data['pedido_aguardo']  = usuario_tem_pedido_em_aguardo
    data['form']            = form
    data['email']           = descriptarAESGCM(usuario.email)
    data['cpf']             = descriptarAESGCM(usuario.cpf)
    data['nascimento']      = descriptarAESGCM(usuario.nascimento)
    data['first_name']      = descriptarAESGCM(usuario.first_name)
    data['last_name']       = descriptarAESGCM(usuario.last_name)

    return render(request, 'meus-dados-usuario.html', data)

def retorna_produtos_salvos_usuario(request):
    data = {}

    produtos = request.user.favorito_produto.all()

    produtos = [
        {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'id_empresa': produto.id_empresa.id,
            'ativo': produto.ativo,
            'qtd': produto.qtd,
            'preco': produto.preco,
            'preco_oferta': produto.preco_oferta,
            'porcentagem_desconto': int(((produto.preco - produto.preco_oferta) / produto.preco) * 100) if produto.preco_oferta is not None else None,
            'primeira_imagem_default': settings.MEDIA_URL + 'default_produto.jpg',
            'primeira_imagem': Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first().imagem if Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first() else None,
            'nome_empresa': produto.id_empresa.nome_fantasia,
            'empresa_imagem': produto.id_empresa.imagem_perfil,
            'categorias': produto.categoria_produto.all(),
            'favorito_usuario': produto.favoritos_produtos.filter(id=request.user.id).exists()
        }
        for produto in produtos
    ]

    paginator = Paginator(produtos, 5)
    pages = request.GET.get('page')

    data['produtos'] = paginator.get_page(pages)

    return render(request, 'produtos-salvos-usuario.html', data)

def cria_pedido_lojista_por_usuario(request):
    try:
        if Pedido_Lojista.objects.filter(
            status_pedido='Aguardando avaliação',
            id_usuario=request.user
        ).exists():
            return JsonResponse({'status': 'error', 'message': 'Você já tem um pedido em aberto.'})
        else:
            Pedido_Lojista.objects.create(
                status_pedido='Aguardando avaliação',
                ultimo_pagamento=None,
                ativo=True,
                id_tipo_assinatura=None,
                id_usuario=request.user
            )

            return JsonResponse({'status': 'success', 'message': 'Pedido criado com sucesso.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def explicacao_cadastro(request):
    return render(request, 'explicacao-cadastro-empresa.html')