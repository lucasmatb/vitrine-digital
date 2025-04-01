from django.shortcuts import render, redirect
from empresas.models import Empresa
from produtos.models import Produto, Imagem_Produto
from usuarios.models import Visualizacao_Empresa, Visualizacao_Produto
from django.db.models import Count
from django.db.models.functions import Least
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from django.utils.timezone import now

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

def retorna_dashboard_lojista(request, id_empresa):

    data = {}

    data['grafico_um'] = prepara_grafico_um(
        30,
        id_empresa
    )

    data['grafico_dois'] = prepara_grafico_dois(
        30,
        id_empresa
    )

    data['grafico_tres'] = prepara_grafico_tres(
        30,
        id_empresa
    )

    data['grafico_quatro'] = prepara_grafico_quatro(
        30,
        id_empresa
    )

    return render(request, 'dashboard-lojista.html', data)

def prepara_grafico_um(
    numero_dias,
    id_empresa,
):
    data = {}

    hoje = now().date()
    dias = [(hoje - timedelta(days=i)) for i in range((numero_dias-1), -1, -1)]

    visualizacoes = (
        Visualizacao_Empresa.objects
        .filter(id_empresa=id_empresa, created_at__date__gte=dias[0])
        .annotate(data_criacao=TruncDate('created_at'))
        .values("data_criacao")
        .annotate(total=Count("id"))
    )
    
    dados = {v["data_criacao"]: v["total"] for v in visualizacoes}
    
    data['id'] = 1
    data['titulo'] = 'Dias com mais visualização da empresa'
    data['subtitulo'] = 'Visualizações'
    data['data'] = [dados.get(dia, 0) for dia in dias]

    return data
def prepara_grafico_dois(
    numero_dias,
    id_empresa,
):
    data_pesquisa = timezone.localtime() - timedelta(days=numero_dias)
    data = {}

    grafico = Visualizacao_Produto.objects.filter(
        created_at__gte=data_pesquisa,
        id_produto__id_empresa=id_empresa
    ).annotate(
        visualizacoes=Count('id')
    ).values_list('id_produto__nome', 'visualizacoes').order_by('-visualizacoes')[:10]
    
    data['id'] = 2
    data['titulo'] = 'Produtos mais visualizados'
    data['subtitulo'] = 'Visualizações'
    data['data'] = {
        'labels': [x[0] for x in grafico],
        'data': [x[1] for x in grafico]
    }

    return data
def prepara_grafico_tres(
    numero_dias,
    id_empresa,
):
    data = {}

    hoje = now().date()
    dias = [(hoje - timedelta(days=i)) for i in range((numero_dias-1), -1, -1)]
    
    produtos_empresa = Produto.objects.filter(id_empresa=id_empresa).values_list("id", flat=True)
    
    visualizacoes = (
        Visualizacao_Produto.objects
        .filter(id_produto__in=produtos_empresa, created_at__date__gte=dias[0])
        .annotate(data_criacao=TruncDate('created_at'))
        .values("data_criacao")
        .annotate(total=Count("id"))
    )
    
    dados = {v["data_criacao"]: v["total"] for v in visualizacoes}
    
    data['id'] = 3
    data['titulo'] = 'Dias com mais visualização de produtos'
    data['subtitulo'] = 'Visualizações'
    data['data'] = [dados.get(dia, 0) for dia in dias]

    return data

def prepara_grafico_quatro(
    numero_dias,
    id_empresa,
):
    data_pesquisa = timezone.localtime() - timedelta(days=numero_dias)
    data = {}

    grafico = Produto.objects.filter(
        id_empresa=id_empresa,
        created_at__gte=data_pesquisa
    ).annotate(
        curtidas=Count('favoritos_produtos')
    ).values_list('nome', 'curtidas').order_by('-curtidas')[:10]

    data['id'] = 4
    data['titulo'] = 'Produtos mais salvos'
    data['subtitulo'] = 'Salvos'
    data['data'] = {
        'labels': [x[0] for x in grafico],
        'data': [x[1] for x in grafico]
    }

    return data








