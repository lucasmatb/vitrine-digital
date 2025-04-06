from django import forms
from .models import Empresa, Categoria_Empresa
from PIL import Image
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
import re

class EmpresaForm(forms.ModelForm):
    def validate_link(value):
        try:
            result = urlparse(value)
            if not all([result.scheme, result.netloc]):
                raise ValidationError("Link inválido")
        except ValueError:
            raise ValidationError("Link inválido")

    cep = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'cep',
            'name': 'cep',
            'placeholder': 'Busque por aqui primeiro!'
        })
    )
    numero = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'numero',
            'name': 'numero',
            'placeholder': '1234'
        })
    )
    logradouro = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'logradouro',
            'name': 'logradouro',
            'readonly': 'readonly'
        })
    )
    complemento = forms.CharField(
        max_length=254,
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'complemento',
            'name': 'complemento',
            'placeholder': 'Próximo ao mercado...'
        })
    )
    bairro = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'bairro',
            'name': 'bairro',
            'readonly': 'readonly'
        })
    )
    cidade = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'cidade',
            'name': 'cidade',
            'readonly': 'readonly'
        })
    )
    estado = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'estado',
            'name': 'estado',
            'readonly': 'readonly'
        })
    )
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria_Empresa.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'id': 'categorias',
                'name': 'categorias',
                'placeholder': 'Escolha uma categoria...',
                'class':"form-control",
                'style':"font-size: 1.5rem;"
            }
        ),
        required=True
    )

    imagem_capa = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'id': 'imagem_capa',
            'class': 'form-control mb-4',
            'placeholder': 'Carregue uma imagem de capa',
            'accept': 'image/png, image/jpg, image/jpeg',
            'onchange': 'exibirImagem(event, "imagem-capa")',
            'onclick': 'verificaExistenciaImagem(event, "imagem-capa")'
        })
    )

    imagem_perfil = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'imagem_perfil',
            'class': 'form-control mb-4',
            'placeholder': 'Carregue uma imagem de perfil',
            'accept': 'image/png, image/jpg, image/jpeg',
            'onchange': 'exibirImagem(event, "imagem-perfil")',
            'onclick': 'verificaExistenciaImagem(event, "imagem-perfil")'
        })
    )

    cnpj_alterado = forms.CharField(
        label=("CNPJ"),
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'cnpj',
            'name': 'cnpj',
            'placeholder': '00.000.000/0000-00'
        })
    )

    telefone = forms.CharField(
        label=("Telefone"),
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'telefone',
            'name': 'telefone',
            'placeholder': '(48) 99999-9999'
        })
    )

    link_whatsapp = forms.CharField(
        label=("Link WhatsApp"),
        max_length=254,
        required=False,
        validators=[validate_link],
        widget=forms.TextInput(attrs={
            'id': 'link_whatsapp',
            'name': 'link_whatsapp'
        })
    )

    link_instagram = forms.CharField(
        label=("Link Instagram"),
        max_length=254,
        required=False,
        validators=[validate_link],
        widget=forms.TextInput(attrs={
            'id': 'link_instagram',
            'name': 'link_instagram'
        })
    )

    link_facebook = forms.CharField(
        label=("Link Facebook"),
        max_length=254,
        required=False,
        validators=[validate_link],
        widget=forms.TextInput(attrs={
            'id': 'link_facebook',
            'name': 'link_facebook'
        })
    )

    def clean(self):
        cleaned_data = super(EmpresaForm, self).clean()

        campos = [
            'cnpj_alterado',
            'nome_fantasia',
            'razao_social',
            'descricao',
            'email',
            'telefone',
            'logradouro',
            'numero',
            'bairro',
            'cep',
            'cidade',
            'estado',
            'categorias',
            'link_whatsapp',
            'link_instagram',
            'link_facebook'
        ]

        for field in campos:
            if cleaned_data.get(field) is None:
                return cleaned_data

        if verifica_cnpj_valido(cleaned_data.get("cnpj_alterado")) is False:
            self.add_error('cnpj_alterado', "CNPJ inválido")
        else:
            cnpjTratado = trata_cnpj_apenas_numeros(cleaned_data.get("cnpj_alterado"))
            if not self.instance.pk and verifica_cnpj_unico(cnpjTratado):
                self.add_error('cnpj_alterado', "CNPJ já cadastrado")
                
            cleaned_data['cnpj_alterado'] = cnpjTratado

            if cleaned_data['imagem_capa'] is None:
                cleaned_data['imagem_capa'] = 'default_capa_empresa.jpg'
            elif verifica_resolucao_imagem(cleaned_data['imagem_capa'], 601, 301):
                self.add_error('imagem_capa', "As imagens devem ter uma resolução maior ou igual a 600x300")
            if cleaned_data['imagem_perfil'] is None:
                cleaned_data['imagem_perfil'] = 'default_perfil_empresa.jpg'
            elif verifica_resolucao_imagem(cleaned_data['imagem_perfil'], 301, 301):
                self.add_error('imagem_perfil', "As imagens devem ter uma resolução maior ou igual a 300x300")

        return cleaned_data

    class Meta:
        model = Empresa
        fields = [
            'cnpj_alterado',
            'nome_fantasia',
            'razao_social',
            'descricao',
            'email',
            'telefone',
            'imagem_capa',
            'imagem_perfil',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cep',
            'cidade',
            'estado',
            'categorias',
            'link_whatsapp',
            'link_instagram',
            'link_facebook'
        ]
    
def verifica_cnpj_valido(formCnpj: str) -> bool:
    cnpj = ''.join(filter(str.isdigit, str(formCnpj)))
    
    if len(cnpj) != 14:
        return False
    
    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj, peso_inicial):
        soma = 0
        peso = peso_inicial
        for i in range(len(cnpj)):
            soma += int(cnpj[i]) * peso
            peso -= 1
            if peso < 2:
                peso = 9
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    primeiro_dv = calcular_digito(cnpj[:12], 5)

    segundo_dv = calcular_digito(cnpj[:12] + primeiro_dv, 6)

    return cnpj[-2:] == primeiro_dv + segundo_dv

def verifica_cnpj_unico(cnpj: str) -> bool:
    return Empresa.objects.filter(cnpj=cnpj).exists()

def trata_cnpj_apenas_numeros(cnpj: str) -> str:
    return re.sub(r'\D', '', cnpj)

def verifica_resolucao_imagem(imagem, largura, altura) -> bool:
    imagem = Image.open(imagem)
    if imagem.width < largura or imagem.height < altura:
        return True
    
    return False
