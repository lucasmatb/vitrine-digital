from django.db import models

class Estados(models.Model):
    descricao = models.CharField(max_length=255)

class Cidades(models.Model):
    descricao = models.CharField(max_length=255)
    id_estado = models.ForeignKey(
        Estados,
        on_delete=models.PROTECT
    )

class Enderecos(models.Model):
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    id_cidade = models.ForeignKey(
        Cidades,
        on_delete=models.PROTECT
    )
    ativo = models.BooleanField()

class Empresas(models.Model):
    cnpj = models.CharField(max_length=14)
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    ativo = models.BooleanField()
    situacao = models.CharField(max_length=30)
    enderecos = models.ManyToManyField(Enderecos)