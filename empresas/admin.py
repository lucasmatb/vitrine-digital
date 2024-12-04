from django.contrib import admin
from .forms import EmpresaRegistrationAdminForm, EmpresaChangeAdminForm
from .models import Estado, Cidade, Endereco, Empresa, Categoria_Empresa

class EmpresaAdmin(admin.ModelAdmin):
    add_form = EmpresaRegistrationAdminForm
    form =  EmpresaChangeAdminForm
    model = Empresa

    fieldsets = (
        (None, {'fields': (
            'cnpj',
            'nome_fantasia',
            'razao_social',
            'id_usuario_descriptografado',
            'ativo',
            'situacao',
        )}),
        ('Contato', {'fields': (
            'email',
            'telefone',
        )}),
        ('Imagens', {'fields': (
            'imagem_capa',
            'imagem_perfil',
        )}),
        ('Categorias', {'fields': (
            'empresa_categoria',
        )}),
        ('Endereços', {'fields': (
            'empresa_endereco',
        )})
    )

    add_fieldsets = (
        (None, {'fields': (
            'cnpj',
            'nome_fantasia',
            'razao_social',
            'id_usuario_descriptografado',
            'ativo',
            'situacao',
        )}),
        ('Contato', {'fields': (
            'email',
            'telefone',
        )}),
        ('Imagens', {'fields': (
            'imagem_capa',
            'imagem_perfil',
        )}),
        ('Categorias', {'fields': (
            'empresa_categoria',
        )}),
        ('Endereços', {'fields': (
            'empresa_endereco',
        )})
    )

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Endereco)
admin.site.register(Categoria_Empresa)