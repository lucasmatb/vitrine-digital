from django.contrib import admin
from .models import Estados, Cidades, Enderecos, Empresas

admin.site.register(Estados)
admin.site.register(Cidades)
admin.site.register(Enderecos)
admin.site.register(Empresas)