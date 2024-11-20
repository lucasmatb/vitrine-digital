from django.core.management.base import BaseCommand
from django_seed import Seed
from usuarios.models import Usuario
from empresas.models import Endereco, Categoria_Empresa, Empresa, Cidade
from produtos.models import Categoria_Produto, Imagem_Produto, Produto

class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        print("seed")
        seeder = Seed.seeder()
        seeder.add_entity(Endereco, 1, {
            'id_cidade': Cidade.objects.get(id=1)
        })
        seeder.add_entity(Categoria_Empresa, 5, {
            'cor': '#FF0000'
        })
        seeder.add_entity(Empresa, 1, {
            'cnpj': '00.000.000/0001-00',
            'situacao': 'Ativo',
            'telefone': '48999998888',
            'id_usuario': Usuario.objects.get(id=1)
        })
        seeder.execute()

        seeder = Seed.seeder()

        seeder.add_entity(Categoria_Produto, 5)
        seeder.add_entity(Imagem_Produto, 5)
        seeder.add_entity(Produto, 1, {
            'id_empresa': Empresa.objects.get(id=1)
        })
        seeder.execute()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
