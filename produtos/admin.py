from django.contrib import admin
from .models import Produtos, Categorias

class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'preco', 'qtd', 'ativo', 'id_categoria', 'id_empresa')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao', 'ativo')
    list_per_page = 10

admin.site.register(Produtos, ProdutosAdmin)
admin.site.register(Categorias)