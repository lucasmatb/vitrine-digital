from django.db import models
from vitrine_digital.helper import retornaCaminhoImagemAleatorio
from stdimage.models import StdImageField

class Imagem_Produto(models.Model):
    imagem = StdImageField(
        'imagem',
        default='default_produto.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
    )

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
    imagem_produto = models.ManyToManyField(Imagem_Produto)