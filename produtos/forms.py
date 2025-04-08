from django import forms
from produtos.models import Produto, Categoria_Produto
from PIL import Image
from decimal import Decimal, InvalidOperation
import re

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
                'accept': 'image/png, image/jpg, image/jpeg, image/webp'
            }
        ),
        required=False
    )

    preco = forms.CharField(
        label=("Preço"),
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'preco',
            'name': 'preco'
        }),
        max_length=14
    )

    preco_oferta = forms.CharField(
        label=("Preço oferta"),
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'preco_oferta',
            'name': 'preco_oferta'
        }),
        max_length=14
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

    def clean(self):
        cleaned_data = super(ProdutoForm, self).clean()

        imagens = self.files.getlist('imagens')

        if len(imagens) > 3:
            self.add_error('imagens', "Você pode enviar no máximo 3 imagens.")
        
        for imagem in imagens:
            image = Image.open(imagem)
            if image.width < 301 or image.height < 301:
                self.add_error('imagens', "As imagens devem ter uma resolução maior ou igual a 300x300.")

        for imagem in imagens:
            if imagem.size > 2 * 1024 * 1024:
                self.add_error('imagens', "As imagens devem ter um tamanho menor ou igual a 2MB.")
            
        if verifica_preco_tipo_correto(cleaned_data.get('preco')) == None:
            self.add_error('preco', "O preço deve ser um valor válido.")
        else:
            cleaned_data['preco'] = verifica_preco_tipo_correto(cleaned_data.get('preco'))

        if cleaned_data.get('preco_oferta'):
            if verifica_preco_tipo_correto(cleaned_data.get('preco_oferta')) == None:
                self.add_error('preco_oferta', "O preço promocional deve ser um valor válido.")
            else:
                cleaned_data['preco_oferta'] = verifica_preco_tipo_correto(cleaned_data.get('preco_oferta'))
                if cleaned_data.get('preco') < (cleaned_data.get('preco_oferta') * Decimal('1.01')):
                    self.add_error('preco_oferta', "O preço de oferta deve ser, ao menos, 1% menor que o preço normal.")

        if cleaned_data.get('preco_oferta') == '' or cleaned_data.get('preco_oferta') == 0:
            cleaned_data['preco_oferta'] = None

        return cleaned_data
    
def verifica_preco_tipo_correto(valor: str):
    if not re.fullmatch(r"[0-9.,]+", valor):
        return None
    
    cleaned = valor.replace(',', '.').replace(".", "")

    if len(cleaned) < 3:
        cleaned = cleaned.rjust(3, "0")

    normalized = cleaned[:-2] + "." + cleaned[-2:]

    try:
        return Decimal(normalized).normalize()
    except InvalidOperation:
        return None
