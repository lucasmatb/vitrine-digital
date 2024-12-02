from django.contrib import admin
from .models import Produto, Imagem_Produto, Categoria_Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'preco', 'qtd', 'ativo', 'id_empresa')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao', 'ativo')
    list_per_page = 10

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria_Produto)
admin.site.register(Imagem_Produto)