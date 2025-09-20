from django.apps import AppConfig
import os
from django.conf import settings
#from .models import ConfiguracionGeneral
class PlataformaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plataforma'
    
    def ready(self):
        from django.db.models.signals import post_migrate
        from .models import Usuario
        from .choices import obtener_roles_personalizados
        
        def actualizar_choices(**kwargs):
            field = Usuario._meta.get_field('rol')
            field.choices = obtener_roles_personalizados()
        
        post_migrate.connect(actualizar_choices, sender=self)

'''class PruebaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plataforma'
  def ready(self):
        if os.environ.get("RUN_MAIN"):
            conf_global = ConfiguracionGeneral.objects.all().first()
            settings.configure(
                EMAIL_HOST_USER = conf_global.correo,
                EMAIL_HOST_PASSWORD = conf_global.contraseña_correo,  
            ) '''


