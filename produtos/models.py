from django.db import models

class Categorias(models.Model):
    descricao = models.CharField(max_length=255)
    ativo = models.BooleanField()

class Produtos(models.Model):
    descricao = models.CharField(max_length=255)
    preco = models.CharField(max_length=30)
    ativo = models.BooleanField()
    id_categoria = models.ForeignKey(
        Categorias,
        on_delete=models.RESTRICT
    )
    id_empresa = models.ForeignKey(
        'empresas.Empresas',
        on_delete=models.RESTRICT
    )