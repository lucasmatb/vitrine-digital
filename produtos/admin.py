from django.contrib import admin
from .models import Produto, Categoria_Produto

admin.site.register(Categoria_Produto)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False