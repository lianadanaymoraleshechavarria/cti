from django.apps import AppConfig

class InvestigadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investigador'

    def ready(self):
        import investigador.signals