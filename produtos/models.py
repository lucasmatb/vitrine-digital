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

    def __str__(self):
        return self.descricao

class Categoria_Produto(models.Model):
    descricao = models.CharField(max_length=254)
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    def __str__(self):
        return self.descricao

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
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    destaque = models.BooleanField()
    id_empresa = models.ForeignKey(
        'empresas.Empresa',
        on_delete=models.RESTRICT
    )
    categoria_produto = models.ManyToManyField(Categoria_Produto)
    imagem_produto = models.ManyToManyField(Imagem_Produto)
    
    def __str__(self):
        return self.descricao