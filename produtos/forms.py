from django import forms
from produtos.models import Produto, Categoria_Produto
from django.core.exceptions import ValidationError

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
                'accept': 'image/png, image/jpg, image/jpeg'
            }
        ),
        required=False
    )

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'qtd', 'ativo', 'destaque', 'categorias', 'imagens']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_imagens(self):
        imagens = self.files.getlist('imagens')
        if len(imagens) > 3:
            raise ValidationError('Você pode enviar no máximo 3 imagens.')
        return imagens