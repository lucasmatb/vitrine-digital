from django.contrib import admin
from .models import Estado, Cidade, Endereco, Empresa, Categoria_Empresa

admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Endereco)
admin.site.register(Empresa)
admin.site.register(Categoria_Empresa)