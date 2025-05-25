from django.contrib import admin
from .models import Empresa, Categoria_Empresa

admin.site.register(Categoria_Empresa)

@admin.register(Empresa)
class ProdutoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False