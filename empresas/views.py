from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .forms import EmpresaForm
from .models import Empresa, Endereco, Estado, Cidade
from produtos.models import Produto, Imagem_Produto
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import requests
from django.db.models import Count
from django.conf import settings
from usuarios.models import Visualizacao_Empresa
from django.utils import timezone
from django.core.paginator import Paginator

def retorna_cadastro_empresa(request):
    data = {}
    data['form'] = EmpresaForm()
    return render(request, 'formulario-empresa.html', data)

def valida_cadastro_empresa(request):
    empresa_count = Empresa.objects.filter(id_usuario=request.user).count()
    if empresa_count >= 10:
        messages.error(request, 'Você chegou no limite de empresas para sua conta, o limite é 10.')
        return redirect('minhas_empresas_lojista')

    form = EmpresaForm(request.POST, request.FILES or None)
    if form.is_valid():
        estado = retorna_model_estado_por_nome(form.cleaned_data['estado'])
        cidade = retorna_model_cidade(estado, form.cleaned_data['cidade'])

        if estado is None or cidade is None:
            messages.error(request, 'Problema na resolução do endereço, tente novamente mais tarde')
        else:
            empresa = Empresa.objects.create(
                nome_fantasia   =  form.cleaned_data['nome_fantasia'],
                razao_social    =  form.cleaned_data['razao_social'],
                descricao       =  form.cleaned_data['descricao'],
                cnpj            =  form.cleaned_data['cnpj_alterado'],
                telefone        =  form.cleaned_data['telefone'],
                email           =  form.cleaned_data['email'],
                imagem_capa     =  form.cleaned_data['imagem_capa'],
                imagem_perfil   =  form.cleaned_data['imagem_perfil'],
                link_whatsapp   =  form.cleaned_data['link_whatsapp'],
                link_instagram  =  form.cleaned_data['link_instagram'],
                link_facebook   =  form.cleaned_data['link_facebook'],
                id_usuario      =  request.user
            )

            empresa.empresa_categoria.add(*form.cleaned_data['categorias'])

            Endereco.objects.create(
                cep         =  form.cleaned_data['cep'],
                logradouro  =  form.cleaned_data['logradouro'],
                numero      =  form.cleaned_data['numero'],
                complemento =  form.cleaned_data['complemento'],
                bairro      =  form.cleaned_data['bairro'],
                id_cidade   =  cidade,
                id_empresa  =  empresa
            )

            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('minhas_empresas_lojista')

    return render(request, 'formulario-empresa.html', {'form': form})

def retorna_model_estado_por_nome(nomeEstado):
    return Estado.objects.get(descricao=nomeEstado)

def retorna_model_cidade(estado, nomeCidade):
    return Cidade.objects.get(descricao=nomeCidade, id_estado=estado)

def retorna_editar_empresa(request, pk):
    data = {}
    empresa = Empresa.objects.get(pk=pk)
    endereco = Endereco.objects.get(id_empresa=empresa)

    if validacao_usuario_possui_empresa(request.user, pk) == False:
        messages.error(request, 'Esta empresa não pertence ao usuário logado')
        return redirect('minhas_empresas_lojista')

    data['form'] = EmpresaForm(instance=empresa)
    data['form'].fields['cnpj_alterado'].initial = empresa.cnpj
    data['form'].fields['cep'].initial = endereco.cep
    data['form'].fields['logradouro'].initial = endereco.logradouro
    data['form'].fields['numero'].initial = endereco.numero
    data['form'].fields['complemento'].initial = endereco.complemento
    data['form'].fields['bairro'].initial = endereco.bairro
    data['form'].fields['cidade'].initial = endereco.id_cidade
    data['form'].fields['estado'].initial = endereco.id_cidade.id_estado
    data['form'].fields['categorias'].initial = empresa.empresa_categoria.all()
    data['imagem_capa'] = empresa.imagem_capa
    data['imagem_perfil'] = empresa.imagem_perfil
    data['id_empresa'] = empresa.id

    return render(request, 'formulario-empresa.html', data)

def valida_editar_empresa(request, pk):
    data = {}
    empresa = Empresa.objects.get(pk=pk)

    if validacao_usuario_possui_empresa(request.user, pk) == False:
        messages.error(request, 'Esta empresa não pertence ao usuário logado')
        return redirect('minhas_empresas_lojista')

    data['id_empresa'] = empresa.id
    data['imagem_capa'] = empresa.imagem_capa
    data['imagem_perfil'] = empresa.imagem_perfil
    endereco = Endereco.objects.get(id_empresa=empresa)
    form = EmpresaForm(request.POST, request.FILES or None, instance=empresa)
    if form.is_valid():
        estado = retorna_model_estado_por_nome(form.cleaned_data['estado'])
        cidade = retorna_model_cidade(estado, form.cleaned_data['cidade'])

        if estado is None or cidade is None:
            messages.error(request, 'Problema na resolução do endereço, tente novamente mais tarde')
        else:

            if form.cleaned_data['imagem_capa'] is None:
                form.cleaned_data['imagem_capa'] = empresa.imagem_capa
            if form.cleaned_data['imagem_perfil'] is None:
                form.cleaned_data['imagem_perfil'] = empresa.imagem_perfil

            empresa.nome_fantasia   =  form.cleaned_data['nome_fantasia']
            empresa.razao_social    =  form.cleaned_data['razao_social']
            empresa.descricao       =  form.cleaned_data['descricao']
            empresa.cnpj            =  form.cleaned_data['cnpj_alterado']
            empresa.telefone        =  form.cleaned_data['telefone']
            empresa.email           =  form.cleaned_data['email']
            empresa.imagem_capa     =  form.cleaned_data['imagem_capa']
            empresa.imagem_perfil   =  form.cleaned_data['imagem_perfil']
            empresa.link_whatsapp   =  form.cleaned_data['link_whatsapp']
            empresa.link_instagram  =  form.cleaned_data['link_instagram']
            empresa.link_facebook   =  form.cleaned_data['link_facebook']
            empresa.save()
            
            empresa.empresa_categoria.set(form.cleaned_data['categorias'])

            endereco.cep         =  form.cleaned_data['cep']
            endereco.logradouro  =  form.cleaned_data['logradouro']
            endereco.numero      =  form.cleaned_data['numero']
            endereco.complemento =  form.cleaned_data['complemento']
            endereco.bairro      =  form.cleaned_data['bairro']
            endereco.id_cidade   =  cidade
            endereco.save()

            messages.success(request, 'Edição realizada com sucesso!')
            return redirect('minhas_empresas_lojista')

    data['form'] = form
    return render(request, 'formulario-empresa.html', data)

def retorna_visualizar_empresa_usuario(request, id_empresa):
    data = {}

    get_object_or_404(Empresa, pk=id_empresa)

    empresa = Empresa.objects.filter(pk=id_empresa).annotate(
        favoritos=Count('favoritos_empresas')
    ).first()

    endereco = Endereco.objects.filter(id_empresa=empresa).first()

    produtos_destaque = Produto.objects.filter(id_empresa=empresa.id, destaque=True).order_by('descricao')

    produtos_destaque = [
        {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'ativo': produto.ativo,
            'qtd': produto.qtd,
            'preco': produto.preco,
            'preco_oferta': produto.preco_oferta,
            'porcentagem_desconto': int(((produto.preco - produto.preco_oferta) / produto.preco) * 100) if produto.preco_oferta is not None else None,
            'primeira_imagem_default': settings.MEDIA_URL + 'default_produto.jpg',
            'primeira_imagem': Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first().imagem if Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first() else None,
            'categorias': produto.categoria_produto.all(),
            'favorito_usuario': produto.favoritos_produtos.filter(id=request.user.id).exists()
        }
        for produto in produtos_destaque
    ]

    produtos = Produto.objects.filter(id_empresa=empresa.id).order_by('descricao')

    produtos = [
        {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'ativo': produto.ativo,
            'qtd': produto.qtd,
            'preco': produto.preco,
            'preco_oferta': produto.preco_oferta,
            'porcentagem_desconto': int(((produto.preco - produto.preco_oferta) / produto.preco) * 100) if produto.preco_oferta is not None else None,
            'primeira_imagem_default': settings.MEDIA_URL + 'default_produto.jpg',
            'primeira_imagem': Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first().imagem if Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first() else None,
            'categorias': produto.categoria_produto.all(),
            'favorito_usuario': produto.favoritos_produtos.filter(id=request.user.id).exists()
        }
        for produto in produtos
    ]

    empresa.qtd_visualizacoes = empresa.qtd_visualizacoes + 1
    empresa.save()

    hoje = timezone.now()
    ontem = hoje - timezone.timedelta(days=1)

    visualizacao_existente = Visualizacao_Empresa.objects.filter(
        id_empresa=empresa,
        id_usuario=request.user,
        created_at__range=(ontem, hoje)
    ).exists()

    if not visualizacao_existente:
        Visualizacao_Empresa.objects.create(
            id_empresa=empresa,
            id_usuario=request.user
        )

    empresa = {
        'id': empresa.id,
        'nome_fantasia': empresa.nome_fantasia,
        'descricao': empresa.descricao,
        'email': empresa.email,
        'telefone': empresa.telefone,
        'imagem_perfil': empresa.imagem_perfil,
        'imagem_capa': empresa.imagem_capa,
        'link_whatsapp': empresa.link_whatsapp,
        'link_instagram': empresa.link_instagram,
        'link_facebook': empresa.link_facebook,
        'categorias': empresa.empresa_categoria.all(),
        'favorito_usuario': empresa.favoritos_empresas.filter(id=request.user.id).exists(),
        'favoritos': empresa.favoritos
    }
    

    endereco = {
        'cep': endereco.cep,
        'logradouro': endereco.logradouro,
        'numero': endereco.numero,
        'complemento': endereco.complemento,
        'bairro': endereco.bairro,
        'cidade': endereco.id_cidade,
        'uf': endereco.id_cidade.id_estado.uf
    }

    data['empresa'] = empresa
    data['endereco'] = endereco
    data['produtos_destaque'] = produtos_destaque
    data['produtos'] = produtos

    return render(request, 'visualizar-empresa-usuario.html', data)

def retorna_minhas_empresas_lojista(request):
    data = {}
    empresas = Empresa.objects.filter(id_usuario=request.user).prefetch_related('empresa_categoria')
    for empresa in empresas:
        produtos = Produto.objects.filter(id_empresa=empresa.id)
        if produtos.count() == 0:
            empresa.contador_favoritos = 0
            empresa.contador_produtos = 0
            empresa.media_salvamento_produto = 0
        else:
            contador_fav_produtos = 0
            for produto in produtos:
                contador_fav_produtos += produto.favoritos_produtos.count()
            empresa.contador_favoritos = empresa.favoritos_empresas.count()
            empresa.contador_produtos = produtos.count()
            empresa.media_salvamento_produto = round(contador_fav_produtos / produtos.count(), 2)

    paginator = Paginator(empresas, 1)
    pages = request.GET.get('page')

    data['empresas'] = paginator.get_page(pages)

    return render(request, 'minhas-empresas-lojista.html', data)

def verifica_cep(request, cep):
    cep_formatado = cep.replace("-", "")

    url = f'https://viacep.com.br/ws/{cep_formatado}/json/'

    try:
        response = requests.get(url)
        response.raise_for_status()

        dados = response.json()

        if "erro" in dados:
            return JsonResponse({'erro': 'CEP não encontrado'}, status=404)

        return JsonResponse(dados, content_type='application/json')

    except requests.RequestException as e:
        return JsonResponse({'erro': 'Erro ao buscar CEP'}, status=500)
    
def excluir_empresa(request, pk):
    try:
        if validacao_usuario_possui_empresa(request.user, pk) == False:
            return JsonResponse({'status': 'error', 'message': 'Esta empresa não pertence ao usuário logado'})

        empresa = get_object_or_404(Empresa, pk=pk)
        empresa.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def validacao_usuario_possui_empresa(usuario, id_empresa):
    empresa = Empresa.objects.get(pk=id_empresa)
    if empresa.id_usuario != usuario:
        return False
    return True

def favorita_nao_favorita_empresa(request, id_empresa):
    try:
        if request.user.favorito_empresa.filter(id=id_empresa).exists():
            request.user.favorito_empresa.remove(Empresa.objects.get(pk=id_empresa))
            like_string = 'unlike'
        else:
            like_string = 'like'
            request.user.favorito_empresa.add(Empresa.objects.get(pk=id_empresa))
        return JsonResponse({'status': 'success', 'message': like_string})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def salva_nao_salva_produto(request, id_produto):
    try:
        if request.user.favorito_produto.filter(id=id_produto).exists():
            request.user.favorito_produto.remove(Produto.objects.get(pk=id_produto))
            like_string = 'unlike'
        else:
            like_string = 'like'
            request.user.favorito_produto.add(Produto.objects.get(pk=id_produto))

        return JsonResponse({'status': 'success', 'message': like_string})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def busca_cidades_por_estado(request, id_estado):

    estado = get_object_or_404(Estado, pk=id_estado)
    cidades = list(
        Cidade.objects.filter(id_estado=estado).order_by('descricao').values('id', 'descricao')
    )
    return JsonResponse(
        {
            'status': 'success',
            'message': cidades,
        }
    )
