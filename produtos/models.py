from django.db import models
from vitrine_digital.helper import retornaCaminhoImagemAleatorio
from stdimage.models import StdImageField

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
        on_delete=models.CASCADE
    )
    categoria_produto = models.ManyToManyField(Categoria_Produto)
    
    def __str__(self):
        return self.descricao
    
class Imagem_Produto(models.Model):
    id_produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )
    imagem = StdImageField(
        default='default_produto.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
        blank=False,
        verbose_name="Imagem produto"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)