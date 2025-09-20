
from django.core.management.base import BaseCommand
from investigador.models import Area

class Command(BaseCommand):
    help = 'Crear áreas por defecto'

    def handle(self, *args, **kwargs):
        areas_por_defecto = [
            'Área de Ciencias',
            'Área de Artes',
            'Área de Tecnología',
            'Área de Humanidades',
        ]

        for nombre_area in areas_por_defecto:
            Area.objects.get_or_create(nombre_area=nombre_area)  # Evita duplicados

        self.stdout.write(self.style.SUCCESS('Áreas por defecto creadas con éxito.'))
