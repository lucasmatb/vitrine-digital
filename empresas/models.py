from django.db import models
from vitrine_digital.helper import retornaCaminhoImagemAleatorio
from stdimage.models import StdImageField

class Estado(models.Model):
    descricao = models.CharField(max_length=254)

class Cidade(models.Model):
    descricao = models.CharField(max_length=254)
    id_estado = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT
    )

class Endereco(models.Model):
    logradouro = models.CharField(max_length=254)
    numero = models.CharField(max_length=254)
    complemento = models.CharField(max_length=254)
    bairro = models.CharField(max_length=254)
    id_cidade = models.ForeignKey(
        Cidade,
        on_delete=models.PROTECT
    )
    ativo = models.BooleanField()

class Categoria_Empresa(models.Model):
    descricao = models.CharField(max_length=254)
    cor = models.CharField(max_length=254)
    ativo = models.BooleanField()

class Empresa(models.Model):
    cnpj = models.CharField(max_length=14)
    nome_fantasia = models.CharField(max_length=254)
    razao_social = models.CharField(max_length=254)
    ativo = models.BooleanField()
    situacao = models.CharField(max_length=30)
    id_usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.RESTRICT
    )
    imagem_capa = StdImageField(
        'imagem',
        default='default_capa_empresa.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'mid': {'width': 480, 'height': 480, 'crop': True}},
    )
    imagem_perfil = StdImageField(
        'imagem',
        default='default_perfil_empresa.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
    )
    categoria_produto = models.ManyToManyField(Categoria_Empresa)
    empresa_endereco = models.ManyToManyField(Endereco)