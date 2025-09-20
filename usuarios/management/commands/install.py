from typing import Any
from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from plataforma.models import Email

from django.contrib.auth.models import Group

GRUPOS = ["Administración","Investigador","Vicedecano","Vicerrector"]

class Command(BaseCommand):

    help = "Genera el estado Inicial"

    def handle(self, *args: Any, **options: Any):

        for g in GRUPOS:
            if not Group.objects.filter(name=g):
                Group.objects.create(name=g)
                print(f"{g} Creado con éxito")

        if not Usuario.objects.filter(is_superuser=True):
            try:
                usuario = Usuario()
                usuario.username = "admin"
                usuario.set_password("admin")
                usuario.is_staff = True
                usuario.is_superuser = True
                usuario.save()
                usuario.groups.add(Group.objects.get(name="Administración"))
                usuario.save()
                print("Admin creado con exito")
            except Exception as e:
                print(e)
                
        email = Email()
        email.address = "secretariadocenteuho@gmail.com"
        email.smtp_server = "smtp.gmail.com"
        email.smtp_port = 465
        email.smtp_username = "secretariadocenteuho@gmail.com"
        email.smtp_password = "wxeq mujn uogo e lv v"
        email.save()
        
        self.stdout.write("Completado")

