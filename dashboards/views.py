from django.shortcuts import render, redirect
from empresas.models import Empresa
from produtos.models import Produto, Imagem_Produto
from django.db.models import Count
from django.db.models.functions import Least

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_usuario')
    
    return render(request, 'home.html')

def retorna_dashboard_usuario(request):
    data = {}

    pesquisa = request.GET.get('pesquisa')

    if not pesquisa:
        produtos_um = Produto.objects.annotate(
            min_date=Least('created_at', 'updated_at'),
            favoritos=Count('favoritos_produtos')
        ).filter(preco_oferta__isnull=False).order_by('min_date')
        data['produtos_um_titulo'] = 'Essas ofertas acabaram de chegar!'
        data['produtos_um'] = set_favoritos_produto(request, produtos_um)

        empresas_um = Empresa.objects.all().order_by('created_at').annotate(
            favoritos=Count('favoritos_empresas')
        )
        data['empresas_um_titulo'] = 'Essas empresas acabaram de chegar!'
        data['empresas_um'] = set_favoritos_empresa(request, empresas_um)

        produtos_dois = Produto.objects.annotate(
            favoritos=Count('favoritos_produtos', distinct=True)
        ).filter(favoritos__gt=0).order_by('-favoritos', 'nome')
        data['produtos_dois_titulo'] = 'Os produtos mais requisitados!'
        data['produtos_dois'] = set_favoritos_produto(request, produtos_dois)

        empresas_dois = Empresa.objects.annotate(
            favoritos=Count('favoritos_empresas', distinct=True)
        ).order_by('-favoritos', 'nome_fantasia')
        data['empresas_dois_titulo'] = ' As empresas mais curtidas!'
        data['empresas_dois'] = set_favoritos_empresa(request, empresas_dois)

        data['sem_pesquisa'] = True
    else:
        empresas_um = Empresa.objects.filter(nome_fantasia__icontains=pesquisa).order_by('nome_fantasia').annotate(
            favoritos=Count('favoritos_empresas')
        )
        data['empresas_um_titulo']= 'Empresas encontradas'
        data['empresas_um'] = set_favoritos_empresa(request, empresas_um)

        produtos_um = Produto.objects.filter(nome__icontains=pesquisa).order_by('nome').annotate(
            favoritos=Count('favoritos_produtos')
        )
        data['produtos_um_titulo'] = 'Produtos encontrados'
        data['produtos_um'] = set_favoritos_produto(request, produtos_um)

        data['sem_pesquisa'] = False

    return render(request, 'dashboard-usuario.html', data)

def set_favoritos_empresa(request, empresas):

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

    return empresas_com_favoritos

def set_favoritos_produto(request, produtos):

    produtos_com_favoritos = [
        {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco': produto.preco,
            'preco_oferta': produto.preco_oferta,
            'qtd': produto.qtd,
            'ativo': produto.ativo,
            'categorias': produto.categoria_produto.all(),
            'porcentagem_desconto': int(((produto.preco - produto.preco_oferta) / produto.preco) * 100) if produto.preco_oferta is not None else None,
            'primeira_imagem': Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first().imagem if Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first() else None,
            'favorito_usuario': produto.favoritos_produtos.filter(id=request.user.id).exists(),
            'favoritos': produto.favoritos
        }
        for produto in produtos
    ]

    return produtos_com_favoritos

def retorna_dashboard_lojista(request):

    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'dashboard-lojista.html')#, data)