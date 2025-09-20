# crear_departamentos.py
from django.core.management.base import BaseCommand
from investigador.models import Departamento, Area

class Command(BaseCommand):
    help = 'Crear departamentos por defecto'

    def handle(self, *args, **kwargs):
        departamentos_por_defecto = [
            {'nombre_departamento': 'Departamento de Física', 'area': 'Área de Ciencias'},
            {'nombre_departamento': 'Departamento de Pintura', 'area': 'Área de Artes'},
            {'nombre_departamento': 'Departamento de Informática', 'area': 'Área de Tecnología'},
            {'nombre_departamento': 'Departamento de Historia', 'area': 'Área de Humanidades'},
        ]

        for depto in departamentos_por_defecto:
            area, created = Area.objects.get_or_create(nombre_area=depto['area'])
            Departamento.objects.get_or_create(nombre_departamento=depto['nombre_departamento'], area=area)  # Evita duplicados

        self.stdout.write(self.style.SUCCESS('Departamentos por defecto creados con éxito.'))
