from django.contrib import admin
from .models import Produto, Categoria_Produto

admin.site.register(Categoria_Produto)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    exclude = (
        'qtd_visualizacoes',
        'id_empresa'
    )

    def has_add_permission(self, request):
        return False