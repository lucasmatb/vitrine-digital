from django import forms
from .models import Usuario
from vitrine_digital.helper import descriptarAESGCM
import re

class UsuarioLoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'email',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

class UsuarioRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'first_name',
            'name': 'first_name',
            'placeholder': 'João'
        })
    )
    last_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'last_name',
            'name': 'last_name',
            'placeholder': 'Silva'
        })
    )
    cpf = forms.CharField(
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'cpf',
            'name': 'cpf',
            'placeholder': '000.000.000-00'
        })
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'email',
            'name': 'email',
            'placeholder': 'joaodasilva@email.com'
        })
    )
    password= forms.CharField(
        widget=forms.PasswordInput(),
        max_length=254,
        required=True
    )
    confirm_password= forms.CharField(
        widget=forms.PasswordInput(),
        max_length=254,
        required=True
    )
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'cpf', 'email', 'password']
    
    def clean(self):
        cleaned_data = super(UsuarioRegistrationForm, self).clean()

        cpfTratado = trata_cpf_apenas_numeros(cleaned_data.get("cpf"))

        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error('confirm_password', "As senhas não coincidem")
        if verifica_email_unico(cleaned_data.get("email")):
            self.add_error('email', "Email já cadastrado")
        if verifica_cpf_valido(cleaned_data.get("cpf")):
            self.add_error('cpf', "CPF inválido")
        if verifica_cpf_unico(cpfTratado):
            self.add_error('cpf', "CPF já cadastrado")
            
        cleaned_data['cpf'] = cpfTratado

        return cleaned_data

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