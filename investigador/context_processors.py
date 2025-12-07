from .models import Notificacion

def notificaciones_context(request):
    if not request.user.is_authenticated:
        return {}

    no_leidas = Notificacion.objects.filter(usuario=request.user, leida=False)

    return {
        'tiene_notificaciones_no_leidas': no_leidas.exists(),
        'contador_notificaciones_no_leidas': no_leidas.count(),
        'notificaciones_user': no_leidas
    }
