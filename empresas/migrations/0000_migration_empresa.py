from django.db import migrations
from empresas.migrations.seed.estados_cidades import retorna_estados, retorna_cidades

def add_estados(apps, schema_editor):
    Estado = apps.get_model('empresas', 'Estado')
    
    Estado.objects.bulk_create(retorna_estados(apps))

def add_cidades(apps, schema_editor):
    Cidade = apps.get_model('empresas', 'Cidade')
    
    Cidade.objects.bulk_create(retorna_cidades(apps))

class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_estados),
        migrations.RunPython(add_cidades)
    ]
