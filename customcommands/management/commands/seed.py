from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        if not Usuario.objects.filter(field1="value1").exists():
            Usuario.objects.create(field1="value1", field2="value2")
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
