from django import forms
from .models import Usuario
from vitrine_digital.helper import encriptarAESGCM, descriptarAESGCM
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserChangeForm
import re

class UsuarioLoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'email',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={
            'id': 'password',
            'name': 'password',
            'autocomplete': 'on'
        })
        }

class UsuarioRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label=("Primeiro nome"),
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'first_name',
            'name': 'first_name',
            'placeholder': 'João'
        })
    )
    last_name = forms.CharField(
        label=("Último nome"),
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'last_name',
            'name': 'last_name',
            'placeholder': 'Silva'
        })
    )
    cpf = forms.CharField(
        label=("CPF"),
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'cpf',
            'name': 'cpf',
            'placeholder': '000.000.000-00'
        })
    )
    email = forms.EmailField(
        label=("E-mail"),
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'email',
            'name': 'email',
            'placeholder': 'joaodasilva@email.com'
        })
    )
    password= forms.CharField(
        label=("Senha"),
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'name': 'password',
            'autocomplete': 'on'
        }),
        max_length=254,
        required=True
    )
    confirm_password= forms.CharField(
        label=("Confirmar senha"),
        widget=forms.PasswordInput(attrs={
            'id': 'confirm-password',
            'name': 'confirm-password',
            'autocomplete': 'on'
        }),
        max_length=254,
        required=True
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'cpf', 'email', 'password']
    
    def clean(self):
        return custom_clean(
            self,
            UsuarioRegistrationForm,
            ['first_name', 'last_name', 'cpf', 'email', 'password'],
            False
        )
    
class UsuarioAdminRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label=("Primeiro nome"),
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'first_name',
            'name': 'first_name',
            'placeholder': 'João'
        })
    )
    last_name = forms.CharField(
        label=("Último nome"),
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'last_name',
            'name': 'last_name',
            'placeholder': 'Silva'
        })
    )
    cpf = forms.CharField(
        label=("CPF"),
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'cpf',
            'name': 'cpf',
            'placeholder': '000.000.000-00'
        })
    )
    email = forms.EmailField(
        label=("E-mail"),
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'email',
            'name': 'email',
            'placeholder': 'joaodasilva@email.com'
        })
    )
    password= forms.CharField(
        label=("Senha"),
        widget=forms.PasswordInput(),
        max_length=254,
        required=True
    )
    confirm_password= forms.CharField(
        label=("Confirmar senha"),
        widget=forms.PasswordInput(),
        max_length=254,
        required=True
    )
    is_staff = forms.BooleanField(
        label=("É staff?"),
        required=False,
        widget=forms.HiddenInput()
    )
    is_superuser = forms.BooleanField(
        label=("É superusuário?"),
        required=False,
        widget=forms.HiddenInput()
    )
    groups = forms.ModelMultipleChoiceField(
        label=("Grupos"),
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'cpf', 'email', 'password', 'is_superuser', 'is_staff', 'groups']
    
    def clean(self):
        return custom_clean(
            self,
            UsuarioAdminRegistrationForm,
            ['first_name', 'last_name', 'cpf', 'email', 'password', 'is_superuser', 'is_staff', 'groups'],
            True
        )


class UsuarioChangeForm(UserChangeForm):
    email_descriptografado = forms.EmailField(
        required=False,
        label=("E-mail"),
        max_length=254,
        widget=forms.TextInput(attrs={
            'id': 'email',
            'name': 'email',
            'placeholder': 'joaodasilva@email.com',
            'readonly': 'readonly'
        })
    )
    cpf_descriptografado = forms.CharField(
        required=False,
        label=("CPF"),
        max_length=14,
        widget=forms.TextInput(attrs={
            'id': 'cpf',
            'name': 'cpf',
            'placeholder': '000.000.000-00',
            'readonly': 'readonly'
        })
    )
    is_staff = forms.BooleanField(
        label=("É staff?"),
        required=False,
        widget=forms.HiddenInput()
    )
    is_superuser = forms.BooleanField(
        label=("É superusuário?"),
        required=False,
        widget=forms.HiddenInput()
    )
    groups = forms.ModelMultipleChoiceField(
        label=("Grupos"),
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        super().__init__(*args, **kwargs)

        if instance:
            self.fields['email_descriptografado'].initial = descriptarAESGCM(instance.email)
            self.fields['cpf_descriptografado'].initial = descriptarAESGCM(instance.cpf)

    class Meta:
        model = Usuario
        fields = ['is_superuser', 'is_staff', 'groups']

    def clean(self):
        cleaned_data = super(UsuarioChangeForm, self).clean()
        fields = ['is_superuser', 'is_staff', 'groups']

        for field in fields:
            if cleaned_data.get(field) is None:
                return cleaned_data

        cleaned_data['groups']          =   clean_groups(self, cleaned_data['groups'])
        cleaned_data['is_staff']        =   False
        cleaned_data['is_superuser']    =   False

        admin_group = Group.objects.get(name="Administrador")
        if admin_group in cleaned_data['groups']:
            cleaned_data['is_staff'] = True
            cleaned_data['is_superuser'] = True

        return cleaned_data
    
class UsuarioEditForm(forms.ModelForm):
    password= forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'name': 'password',
            'autocomplete': 'on'
        }),
        max_length=254,
        required=False
    )
    confirm_password= forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'confirm-password',
            'name': 'confirm-password',
            'autocomplete': 'on'
        }),
        max_length=254,
        required=False
    )
    imagem = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'nova-imagem',
            'name': 'nova-imagem',
            'class': 'form-control mb-4',
            'placeholder': 'Carregue uma imagem de perfil',
            'accept': 'image/png, image/jpg, image/jpeg'
        }),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['imagem', 'password', 'confirm_password']
    
    def clean(self):
        cleaned_data = super(UsuarioEditForm, self).clean()
            
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error('confirm_password', "As senhas não coincidem")

        return cleaned_data

def custom_clean(self, forms, campos, admin):
    cleaned_data = super(forms, self).clean()

    for field in campos:
        if cleaned_data.get(field) is None:
            return cleaned_data

    if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
        self.add_error('confirm_password', "As senhas não coincidem")
    if verifica_email_unico(cleaned_data.get("email")):
        self.add_error('email', "Email já cadastrado")
    if verifica_cpf_valido(cleaned_data.get("cpf")):
        self.add_error('cpf', "CPF inválido")
    cpfTratado = trata_cpf_apenas_numeros(cleaned_data.get("cpf"))
    if verifica_cpf_unico(cpfTratado):
        self.add_error('cpf', "CPF já cadastrado")

    if self.errors:
        return cleaned_data
        
    cleaned_data['cpf'] = cpfTratado

    if admin:
        cleaned_data['groups']          =   clean_groups(self, cleaned_data['groups'])
        cleaned_data['email']           =   encriptarAESGCM(cleaned_data['email'])
        cleaned_data['password']        =   make_password(cleaned_data['password'])
        cleaned_data['first_name']      =   encriptarAESGCM(cleaned_data['first_name'])
        cleaned_data['last_name']       =   encriptarAESGCM(cleaned_data['last_name'])
        cleaned_data['cpf']             =   encriptarAESGCM(cleaned_data['cpf'])
        cleaned_data['is_staff']        =   False
        cleaned_data['is_superuser']    =   False

        admin_group = Group.objects.get(name="Administrador")
        if admin_group in cleaned_data['groups']:
            cleaned_data['is_staff'] = True
            cleaned_data['is_superuser'] = True

    return cleaned_data

def clean_groups(self, groups):
    admin_group = Group.objects.get(name="Administrador")
    usuario_group = Group.objects.get(name="Usuário")
    lojista_group = Group.objects.get(name="Lojista")
    
    if admin_group in groups and (usuario_group in groups or lojista_group in groups):
        self.add_error('groups', 'O grupo "Administrador" não pode ser selecionado junto com outros grupos.')
    
    if lojista_group in groups and usuario_group not in groups:
        self.add_error('groups', 'Caso o grupo "Lojista" seja selecionado, o grupo "Usuário" também deve ser selecionado.')

    return groups

def verifica_email_unico(email: str) -> bool:
    emails = [descriptarAESGCM(email) for email in Usuario.objects.values_list('email', flat=True)]
    if email in emails:
        return True

def verifica_cpf_valido(cpf: str):
    if not metodo_padrao_valida_cpf(cpf):
        return True
    
def verifica_cpf_unico(cpf: str):
    cpfs = [descriptarAESGCM(cpf) for cpf in Usuario.objects.values_list('cpf', flat=True)]
    if cpf in cpfs:
        return True
    
def metodo_padrao_valida_cpf(formCpf: str) -> bool:
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', formCpf):
        return False

    numbers = [int(digit) for digit in formCpf if digit.isdigit()]

    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True

def trata_cpf_apenas_numeros(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)