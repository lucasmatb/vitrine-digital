from django.shortcuts import render, redirect
from empresas.models import Empresa, Categoria_Empresa
from usuarios.models import Pedido_Lojista
from django.db.models import Count

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_usuario')
    
    return render(request, 'home.html')

def retorna_dashboard_usuario(request):
    data = {}

    pesquisa = request.GET.get('pesquisa')

    if not pesquisa:
        empresas = Empresa.objects.all().order_by('nome_fantasia').annotate(
            favoritos=Count('favoritos_empresas')
        )
    else:
        empresas = Empresa.objects.filter(nome_fantasia__icontains=pesquisa).order_by('nome_fantasia').annotate(
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

    data['empresas'] = empresas_com_favoritos

    return render(request, 'dashboard-usuario.html', data)

def retorna_dashboard_lojista(request):

    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'dashboard-lojista.html')#, data)