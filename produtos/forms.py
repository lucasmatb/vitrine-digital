from django import forms
from produtos.models import Produto, Categoria_Produto
from django.core.exceptions import ValidationError
from PIL import Image
from decimal import Decimal

class ProdutoForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria_Produto.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'id': 'categorias',
                'name': 'categorias',
                'placeholder': 'Escolha uma categoria...',
                'style':"font-size: 1.5rem;"
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

    preco = forms.DecimalField(
        label=("Preço"),
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'preco',
            'name': 'preco'
        }),
        decimal_places=2,
        max_digits=8
    )

    preco_oferta = forms.DecimalField(
        label=("Preço oferta"),
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'preco_oferta',
            'name': 'preco_oferta'
        }),
        decimal_places=2,
        max_digits=8
    )

    qtd = forms.IntegerField(
        label=("Quantidade"),
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'quantidade',
            'name': 'quantidade'
        }),
        min_value=1,
        max_value=999
    )

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'preco_oferta', 'qtd', 'ativo', 'destaque', 'categorias', 'imagens']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_imagens(self):
        imagens = self.files.getlist('imagens')
        if len(imagens) > 3:
            raise ValidationError('Você pode enviar no máximo 3 imagens.')
        for imagem in imagens:
            image = Image.open(imagem)
            if image.width < 300 or image.height < 300:
                raise ValidationError('As imagens devem ter uma resolução maior ou igual a 300x300.')
        
        return imagens
    
    def clean_preco_oferta(self):
        preco = self.cleaned_data.get('preco')
        preco_oferta = self.cleaned_data.get('preco_oferta')
        if preco_oferta and preco < (preco_oferta * Decimal('1.01')):
            raise ValidationError('O preço de oferta deve ser menor que o preço normal.')
        
        return preco_oferta