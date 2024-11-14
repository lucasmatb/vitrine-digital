from django.db import models

class Categoria_Produto(models.Model):
    descricao = models.CharField(max_length=254)
    ativo = models.BooleanField()

class Produto(models.Model):
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
    destaque = models.BooleanField()
    id_empresa = models.ForeignKey(
        'empresas.Empresa',
        on_delete=models.RESTRICT
    )
    id_categoria_produto = models.ForeignKey(
        Categoria_Produto,
        on_delete=models.RESTRICT
    )