from django import forms
from produtos.models import Produto, Categoria_Produto

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
    imagens = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'id': 'imagens',
                'name': 'imagens',
                'allow_multiple_selected': True,
                'multiple': True,
                'accept': 'image/png, image/jpg, image/jpeg',
                'required': 'required'
            }
        )
    )

    class Meta:
        model = Produto
        fields = ['descricao', 'preco', 'qtd', 'ativo', 'destaque', 'categorias', 'imagens']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'