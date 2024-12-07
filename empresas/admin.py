from django.contrib import admin
from .models import Estado, Cidade, Categoria_Empresa

admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Categoria_Empresa)