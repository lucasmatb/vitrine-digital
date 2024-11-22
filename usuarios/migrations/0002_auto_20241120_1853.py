from django.db import migrations
from usuarios.migrations.seed.permissoes_grupos import (
    retorna_permissoes_grupo_administrador,
    retorna_permissoes_grupo_usuario,
    retorna_permissoes_grupo_lojista
)

from django.db import migrations

def criar_grupo_com_permissoes_admin(apps, schema_editor):
    # Importando os modelos de Grupo e Permissões
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Nome do grupo a ser criado
    grupo_permissoes_administrador = 'Administrador'

    # Lista de permissões que o grupo deve ter (codename das permissões)
    permissoes_codenames = retorna_permissoes_grupo_administrador()

    grupo, criado = Group.objects.get_or_create(name=grupo_permissoes_administrador)

    permissoes = Permission.objects.filter(codename__in=permissoes_codenames)

    grupo.permissions.set(permissoes)

def criar_grupo_com_permissoes_usuario(apps, schema_editor):
    # Importando os modelos de Grupo e Permissões
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Nome do grupo a ser criado
    grupo_permissoes_usuario = 'Usuário'

    # Lista de permissões que o grupo deve ter (codename das permissões)
    permissoes_codenames = retorna_permissoes_grupo_usuario()

    grupo, criado = Group.objects.get_or_create(name=grupo_permissoes_usuario)

    permissoes = Permission.objects.filter(codename__in=permissoes_codenames)

    grupo.permissions.set(permissoes)

def criar_grupo_com_permissoes_lojista(apps, schema_editor):
    # Importando os modelos de Grupo e Permissões
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Nome do grupo a ser criado
    grupo_permissoes_lojista = 'Lojista'

    # Lista de permissões que o grupo deve ter (codename das permissões)
    permissoes_codenames = retorna_permissoes_grupo_lojista()

    grupo, criado = Group.objects.get_or_create(name=grupo_permissoes_lojista)

    permissoes = Permission.objects.filter(codename__in=permissoes_codenames)

    grupo.permissions.set(permissoes)

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_grupo_com_permissoes_admin),
        migrations.RunPython(criar_grupo_com_permissoes_usuario),
        migrations.RunPython(criar_grupo_com_permissoes_lojista)
    ]
