from django import forms
from .models import Empresa, Endereco, Categoria_Empresa, Estado, Cidade
from django.forms import inlineformset_factory
from usuarios.models import Usuario
from vitrine_digital.helper import descriptarAESGCM

class EmpresaRegistrationForm(forms.ModelForm):

    logradouro = forms.CharField(
        max_length=254,
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'logradouro',
            'name': 'logradouro',
            'placeholder': 'Rua das couves'
        })
    )
    numero = forms.CharField(
        max_length=254,
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'numero',
            'name': 'numero',
            'placeholder': '1234'
        })
    )
    complemento = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'complemento',
            'name': 'complemento',
            'placeholder': 'Próximo ao mercado...'
        })
    )
    bairro = forms.CharField(
        max_length=254,
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'bairro',
            'name': 'bairro',
            'placeholder': 'Humaitá'
        })
    )
    cep = forms.CharField(
        max_length=254,
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'cep',
            'name': 'cep',
            'placeholder': '88888-000'
        })
    )
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.none(),
        empty_label="Selecione uma cidade",
        widget=forms.Select(
            attrs={
                'id': 'cidade',
                'name': 'cidade',
                'placeholder': 'Araranguá'
            }
        )
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        empty_label="Selecione um Estado",
        widget=forms.Select(
            attrs={
                'id': 'estado',
                'name': 'estado',
                'placeholder': 'Santa Catarina'
            }
        )
    )
    categorias = forms.MultipleChoiceField(
        choices=Categoria_Empresa.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'categorias',
                'name': 'categorias',
                'placeholder': 'Roupas...'
            }
        )
    )
    class Meta:
        model = Empresa
        fields = [
            'cnpj',
            'nome_fantasia',
            'razao_social',
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
        ]

class EmpresaRegistrationAdminForm(forms.ModelForm):

    id_usuario_descriptografado = forms.MultipleChoiceField(
        choices=[(email, email) for email in [descriptarAESGCM(e) for e in Usuario.objects.values_list('email', flat=True)]],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude = ['id_usuario']

class EmpresaChangeAdminForm(forms.ModelForm):

    id_usuario_descriptografado = forms.MultipleChoiceField(
        choices=[(email, email) for email in [descriptarAESGCM(e) for e in Usuario.objects.values_list('email', flat=True)]],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude = ['id_usuario']

class CategoriaEmpresaForm(forms.ModelForm):
    class Meta:
        model = Categoria_Empresa
        fields = ['descricao']  # Inclua os campos necessários

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'id_cidade']