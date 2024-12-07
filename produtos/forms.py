from django import forms
from produtos.models import Produto, Categoria_Produto, Imagem_Produto
from django.forms import modelformset_factory

class ImagemProdutoForm(forms.ModelForm):
    class Meta:
        model = Imagem_Produto
        fields = ['imagem']

class ProdutoForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria_Produto.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'id': 'categorias',
                'name': 'categorias',
                'placeholder': 'Escolha uma categoria...'
            }
        ),
        required=True
    )

    class Meta:
        model = Produto
        fields = ['descricao', 'preco', 'qtd', 'ativo', 'destaque', 'id_empresa', 'categorias']

ImagemProdutoFormSet = modelformset_factory(
    Imagem_Produto,
    form=ImagemProdutoForm,
    extra=1
)