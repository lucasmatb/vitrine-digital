from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from empresas.models import Empresa
from produtos.models import Produto
from vitrine_digital.helper import retornaCaminhoImagemAleatorio
from stdimage.models import StdImageField
from vitrine_digital.helper import descriptarAESGCM
from empresas.models import Cidade
from vitrine_digital.models import BaseModel

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    email = models.CharField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name="E-mail"
    )

    first_name = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Primeiro nome"
    )

    last_name = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Último nome"
    )

    is_staff = models.BooleanField(
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
        verbose_name="É staff?"
    )

    is_active = models.BooleanField(
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
        verbose_name="Ativo"
    )
    
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de criação"
    )

    cpf = models.CharField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name="CPF"
    )

    imagem = StdImageField(
        verbose_name="imagem",
        default='default_profile.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
        blank=False
    )

    favorito_produto = models.ManyToManyField(
        Produto,
        related_name='favoritos_produtos'
    )
    favorito_empresa = models.ManyToManyField(
        Empresa,
        related_name='favoritos_empresas'
    )

    visualizacao_empresa = models.ManyToManyField(
        Empresa,
        related_name='visualizacoes_empresas'
    )
    visualizacao_produto = models.ManyToManyField(
        Produto,
        related_name='visualizacoes_produtos'
    )

    id_cidade = models.ForeignKey(
        Cidade,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=True,
        verbose_name="Cidade para pesquisa"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf']
    
    def __str__(self):
        return descriptarAESGCM(self.email)
    
class Tipo_Assinatura(BaseModel):
    descricao = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Descrição"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    def __str__(self):
        return self.descricao

class Pedido_Lojista(BaseModel):
    status_pedido = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Estado do pedido"
    )
    ultimo_pagamento = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data do último pagamento"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    id_tipo_assinatura = models.ForeignKey(
        Tipo_Assinatura,
        null=True,
        on_delete=models.DO_NOTHING
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.status_pedido
    
class Visualizacao_Empresa(BaseModel):
    id_empresa = models.ForeignKey(
        Empresa,
        on_delete=models.DO_NOTHING
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        related_name='visualizacao_empresa_usuario'
    )
class Visualizacao_Produto(BaseModel):
    id_produto = models.ForeignKey(
        Produto,
        on_delete=models.DO_NOTHING
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        related_name='visualizacao_produto_usuario'
    )