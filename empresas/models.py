from django.db import models
from vitrine_digital.helper import retornaCaminhoImagemAleatorio
from stdimage.models import StdImageField

class Estado(models.Model):
    descricao = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Descrição"
    )
    uf = models.CharField(
        max_length=2,
        blank=False,
        verbose_name="UF"
    )

    def __str__(self):
        return self.descricao

class Cidade(models.Model):
    descricao = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Descrição"
    )
    id_estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Estado"
    )

    def __str__(self):
        return self.descricao

class Categoria_Empresa(models.Model):
    descricao = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Descrição"
    )
    cor = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Cor"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    def __str__(self):
        return self.descricao

class Empresa(models.Model):
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        blank=False,
        verbose_name="CNPJ"
    )
    nome_fantasia = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Nome fantasia"
    )
    razao_social = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Razão social"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        verbose_name="E-mail"
    )
    telefone = models.CharField(
        max_length=30,
        blank=False,
        verbose_name="Telefone"
    )
    id_usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.DO_NOTHING,
        blank=False
    )
    imagem_capa = StdImageField(
        default='default_capa_empresa.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'mid': {'width': 480, 'height': 480, 'crop': True}},
        blank=False,
        verbose_name="Imagem capa"
    )
    imagem_perfil = StdImageField(
        default='default_perfil_empresa.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
        blank=False,
        verbose_name="Imagem perfil"
    )
    empresa_categoria = models.ManyToManyField(Categoria_Empresa)

    def __str__(self):
        return self.nome_fantasia
    
class Endereco(models.Model):
    cep = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="CEP"
    )
    logradouro = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Logradouro"
    )
    numero = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Número"
    )
    complemento = models.CharField(
        max_length=254,
        blank=True,
        verbose_name="Complemento"
    )
    bairro = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Bairro"
    )
    id_cidade = models.ForeignKey(
        Cidade,
        on_delete=models.DO_NOTHING,
        blank=False,
        verbose_name="Cidade"
    )
    id_empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Empresa"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    def __str__(self):
        return self.logradouro