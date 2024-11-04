from django.db import models

class Categorias(models.Model):
    descricao = models.CharField(max_length=254)
    ativo = models.BooleanField()

class Produtos(models.Model):
    descricao = models.CharField(
        'Descrição do produto',
        max_length=254
    )
    preco = models.DecimalField(
        'Preço do produto',
        decimal_places=2,
        max_digits=8
    )
    qtd = models.IntegerField(
        'Quantidade em estoque',
        default=0
    )
    ativo = models.BooleanField()
    id_categoria = models.ForeignKey(
        Categorias,
        on_delete=models.RESTRICT
    )
    id_empresa = models.ForeignKey(
        'empresas.Empresas',
        on_delete=models.RESTRICT
    )