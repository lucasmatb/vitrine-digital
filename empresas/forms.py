from django import forms
from .models import Empresa
from usuarios.models import Usuario
from vitrine_digital.helper import descriptarAESGCM

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