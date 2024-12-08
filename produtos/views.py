from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Produto, Imagem_Produto
from .forms import ProdutoForm, ImagemProdutoFormSet
def retorna_visualizar_produto(request):
    return render(request, 'visualizar-produto.html')

def retorna_listagem_produtos_por_empresa(request, id_empresa):
    return render(request, 'visualizar-produto.html')

def criar_produto(request):
    if request.method == 'POST':
        produto_form = ProdutoForm(request.POST)
        formset = ImagemProdutoFormSet(request.POST, request.FILES)

        if produto_form.is_valid() and formset.is_valid():
            produto = produto_form.save()

            for form in formset:
                imagem = form.save(commit=False)
                imagem.produto = produto
                imagem.save()

            return JsonResponse({'success': True, 'id': produto.id, 'nome': produto.nome})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Método não permitido'})

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':

        produto_form = ProdutoForm(request.POST, instance=produto)
        formset = ImagemProdutoFormSet(request.POST, request.FILES, queryset=Imagem_Produto.objects.filter(produto=produto))

        if produto_form.is_valid() and formset.is_valid():
            produto = produto_form.save()

            for form in formset:
                imagem = form.save(commit=False)
                imagem.produto = produto
                if imagem.imagem:  # Se houver uma nova imagem, ela será salva
                    imagem.save()
            return JsonResponse({'success': True, 'id': produto.id, 'nome': produto.nome})
        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'errors': 'Método não permitido'})

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    return JsonResponse({'success': True})