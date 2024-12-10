from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Tipo_Assinatura, Pedido_Lojista
from .forms import UsuarioAdminRegistrationForm, UsuarioChangeForm
from vitrine_digital.helper import descriptarAESGCM

# Personalize os textos do Admin0
admin.site.site_title = "Vitrine Digital"  # Título da aba do navegador
admin.site.site_header = "Gerenciamento da plataforma"  # Cabeçalho principal
admin.site.index_title = "Painel Administrativo"  # Subtítulo na página inicial

class MyUserAdmin(UserAdmin):
    add_form = UsuarioAdminRegistrationForm
    form =  UsuarioChangeForm
    model = Usuario

    # Descriptografa o e-mail
    def email_descriptografado(self, obj):
        return descriptarAESGCM(obj.email)
    email_descriptografado.short_description = "E-mail"

    # Descriptografa o primeiro nome
    def primeiro_nome_descriptografado(self, obj):
        return descriptarAESGCM(obj.first_name)
    primeiro_nome_descriptografado.short_description = "Primeiro Nome"

    # Descriptografa o último nome
    def ultimo_nome_descriptografado(self, obj):
        return descriptarAESGCM(obj.last_name)
    ultimo_nome_descriptografado.short_description = "Último Nome"

    # Descriptografa o CPF
    def cpf_descriptografado(self, obj):
        return descriptarAESGCM(obj.cpf)
    cpf_descriptografado.short_description = "CPF"

    def grupos(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    grupos.short_description = "Grupos"  # Nome da coluna no admin

    list_display = [
        'email_descriptografado',
        'primeiro_nome_descriptografado',
        'ultimo_nome_descriptografado',
        'cpf_descriptografado',
        'is_active',
        'is_superuser',
        'grupos'
    ]
    
    ordering = ['is_superuser']

    fieldsets = (
        (None, {'fields': ('email_descriptografado', 'cpf_descriptografado')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')})
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'confirm_password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'cpf')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')})
    )

    list_filter = ("is_superuser", "is_active", "groups")  # Filtros padrão e adicionais

class MyPedidoLojistaAdmin(admin.ModelAdmin):

    def email_descriptografado(self, obj):
        return descriptarAESGCM(obj.id_usuario.email)
    email_descriptografado.short_description = "E-mail"

    list_display = [
        'email_descriptografado',
        'status_pedido',
        'ultimo_pagamento',
        'ativo',
        'id_tipo_assinatura'
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # Check if it's an edit action
            form.base_fields.pop('id_usuario', None)
        return form
    
    ordering = ['status_pedido']

    list_filter = ("status_pedido", "ultimo_pagamento", "ativo")

admin.site.register(Usuario, MyUserAdmin)
admin.site.register(Tipo_Assinatura)
admin.site.register(Pedido_Lojista, MyPedidoLojistaAdmin)