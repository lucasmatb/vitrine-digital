# Generated by Django 3.1.4 on 2024-10-12 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('ativo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('preco', models.CharField(max_length=30)),
                ('ativo', models.BooleanField()),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produtos.categorias')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='empresas.empresas')),
            ],
        ),
    ]
