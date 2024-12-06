from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from empresas.models import Empresa
from produtos.models import Produto
from vitrine_digital.helper import retornaCaminhoImagemAleatorio
from stdimage.models import StdImageField

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
        'imagem',
        default='default_profile.jpg',
        upload_to=retornaCaminhoImagemAleatorio,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
    )

    favorito_produto = models.ManyToManyField(Produto)
    favorito_empresa = models.ManyToManyField(Empresa)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf']
    
    def __str__(self):
        return self.email
    
class Tipo_Assinatura(models.Model):
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

class Pedido_Lojista(models.Model):
    status_pedido = models.CharField(
        max_length=254,
        blank=False,
        verbose_name="Estado do pedido"
    )
    ultimo_pagamento = models.DateTimeField(
        blank=False,
        verbose_name="Data do último pagamento"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    id_tipo_assinatura = models.ForeignKey(
        Tipo_Assinatura,
        on_delete=models.RESTRICT
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.status_pedido