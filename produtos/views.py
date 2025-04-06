from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Produto, Imagem_Produto
from .forms import ProdutoForm
from django.shortcuts import redirect
from django.contrib import messages
from empresas.views import validacao_usuario_possui_empresa
from empresas.models import Empresa
from django.conf import settings
from usuarios.models import Visualizacao_Produto
from django.utils.timezone import now

def retorna_visualizar_produto(request, pk):
    data = {}
    produto = get_object_or_404(Produto, id=pk)

    produto.qtd_visualizacoes = produto.qtd_visualizacoes + 1
    produto.save()

    visualizacao_existente = Visualizacao_Produto.objects.filter(
        id_produto=produto,
        id_usuario=request.user,
        created_at__date=now().date()
    ).exists()

    if not visualizacao_existente:
        Visualizacao_Produto.objects.create(
            id_produto=produto,
            id_usuario=request.user
        )

    imagens = Imagem_Produto.objects.filter(id_produto=produto.id)
    produto.primeira_imagem_default = settings.MEDIA_URL + 'default_produto.jpg'

    data['produto'] = produto
    data['imagens_existentes'] = imagens
    data['favorito_usuario'] = produto.favoritos_produtos.filter(id=request.user.id).exists()
    
    return render(request, 'visualizar-produto-usuario.html', data)

def retorna_listagem_produtos_por_empresa(request, id_empresa):
    data = {}
    data['produtos'] = Produto.objects.filter(id_empresa=id_empresa).prefetch_related('categoria_produto')
    for produto in data['produtos']:
        if produto.preco_oferta is not None:
            produto.porcentagem_desconto = int(((produto.preco - produto.preco_oferta) / produto.preco) * 100)
        else:
            produto.porcentagem_desconto = None
        produto.primeira_imagem_default = settings.MEDIA_URL + 'default_produto.jpg'
        try:
            produto.primeira_imagem = Imagem_Produto.objects.filter(id_produto=produto).order_by('id').first().imagem
        except AttributeError:
            produto.primeira_imagem = None
    data['id_empresa'] = id_empresa
    return render(request, 'listagem-produtos-lojista.html', data)

def criar_produto(request, id_empresa):
    data = {}
    data['id_empresa'] = id_empresa

    if validacao_usuario_possui_empresa(request.user, id_empresa) == False:
        messages.error(request, 'Esta empresa não pertence ao usuário logado')
        return redirect('minhas_empresas_lojista')

    produto_count = Produto.objects.filter(id_empresa=id_empresa).count()
    if produto_count >= 50:
        messages.error(request, 'Você chegou no limite de produtos para sua conta, o limite é 50.')
        return redirect('minhas_empresas_lojista')
    
    if request.method == 'POST':

        data_post = request.POST.copy()

        form = ProdutoForm(data_post, request.FILES)

        imagens = request.FILES.getlist('imagens')
        if imagens:
            messages.error(request, 'O produto deve ter pelo menos uma imagem')

        if imagens and form.is_valid():
            empresa = Empresa.objects.get(pk=id_empresa)
            produto = Produto.objects.create(
                nome            =  form.cleaned_data['nome'],
                descricao       =  form.cleaned_data['descricao'],
                preco           =  form.cleaned_data['preco'],
                preco_oferta    =  form.cleaned_data['preco_oferta'],
                qtd             =  form.cleaned_data['qtd'],
                ativo           =  form.cleaned_data['ativo'],
                destaque        =  form.cleaned_data['destaque'],
                id_empresa      =  empresa
            )

            produto.categoria_produto.add(*form.cleaned_data['categorias'])

            if imagens:
                for imagem in imagens:
                    Imagem_Produto.objects.create(
                        id_produto=produto,
                        imagem=imagem
                    )
                
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('listagem_produto_por_empresa', id_empresa=id_empresa)
        else:
            data['form'] = form
    else:
        data['form'] = ProdutoForm()

    return render(request, 'produto-form.html', data)

def editar_produto(request, id_empresa, pk):
    data = {}
    data['id_empresa'] = id_empresa
    data['id_produto'] = pk
    if validacao_usuario_possui_empresa(request.user, id_empresa) == False:
        messages.error(request, 'Este produto não pertence ao usuário logado')
        return redirect('listagem_produto_por_empresa', id_empresa)

    produto = get_object_or_404(Produto, id=pk, id_empresa=id_empresa)

    if request.method == 'POST':
        data_post = request.POST.copy()

        if 'preco' in data_post:
            data_post['preco'] = data_post['preco'].replace(",", ".")

        if 'preco_oferta' in data_post:
            data_post['preco_oferta'] = data_post['preco_oferta'].replace(",", ".")
            if data_post['preco_oferta'] == '0.00':
                data_post['preco_oferta'] = None

        form = ProdutoForm(data_post, request.FILES, instance=produto)

        if form.is_valid():

            produto.nome            =  form.cleaned_data['nome']
            produto.descricao       =  form.cleaned_data['descricao']
            produto.preco           =  form.cleaned_data['preco']
            produto.preco_oferta    =  form.cleaned_data['preco_oferta']
            produto.qtd             =  form.cleaned_data['qtd']
            produto.ativo           =  form.cleaned_data['ativo']
            produto.destaque        =  form.cleaned_data['destaque']
            produto.save()

            produto.categoria_produto.set(form.cleaned_data['categorias'])

            imagens = request.FILES.getlist('imagens')

            if imagens:
                imagens_antigas = Imagem_Produto.objects.filter(id_produto=produto)

                if imagens_antigas:
                    imagens_antigas.delete()

                for imagem in imagens:
                    Imagem_Produto.objects.create(
                        id_produto=produto,
                        imagem=imagem
                    )

            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('listagem_produto_por_empresa', id_empresa=id_empresa)
    else:
        form = ProdutoForm(instance=produto)
        form.fields['categorias'].initial = produto.categoria_produto.all()

    data['imagens_existentes'] = Imagem_Produto.objects.filter(id_produto=produto)
    data['form'] = form
    return render(request, 'produto-form.html', data)

def excluir_produto(request, id_empresa, pk):
    produto = get_object_or_404(Produto, id=pk)
    if validacao_usuario_possui_empresa(request.user, id_empresa) == False:
        messages.error(request, 'Este produto não pertence ao usuário logado')
        return redirect('listagem_produto_por_empresa', id_empresa)

    produto.delete()
    return redirect('listagem_produto_por_empresa', id_empresa)