from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import Articulo, Evento, Premio, Proyecto, Programa, Notificacion
from plataforma.models import Usuario
import logging

logger = logging.getLogger(__name__)

def crear_notificacion_sin_duplicados(modelo, instance):
    """
    Crea notificaciones para vicerrectores y jefes relevantes evitando duplicados
    """
    # Usar transacción para evitar condiciones de carrera
    with transaction.atomic():
        # Determinar el área y departamento del elemento
        area = getattr(instance, 'area', None)
        departamento = getattr(instance, 'departamento', None)
        
        # Buscar destinatarios
        destinatarios = []
        
        # Vicerrectores (todos reciben notificaciones)
        vicerrectores = Usuario.objects.filter(rol='Vicerrector')
        destinatarios.extend(vicerrectores)
        
        # Jefes de área relacionados
        if area:
            jefes_area = Usuario.objects.filter(rol='Jefe_area', area=area)
            destinatarios.extend(jefes_area)
        
        # Jefes de departamento relacionados
        if departamento:
            jefes_departamento = Usuario.objects.filter(rol='Jefe_departamento', departamento=departamento)
            destinatarios.extend(jefes_departamento)
        
        # Determinar el nombre del elemento
        nombre_elemento = ""
        if hasattr(instance, 'titulo'):
            nombre_elemento = instance.titulo
        elif hasattr(instance, 'nombre_proyecto'):
            nombre_elemento = instance.nombre_proyecto
        elif hasattr(instance, 'nombre_programa'):
            nombre_elemento = instance.nombre_programa
        else:
            nombre_elemento = str(instance)
        
        # Crear notificaciones evitando duplicados
        for usuario in destinatarios:
            # Verificación más específica de duplicados
            notificacion_existente = Notificacion.objects.filter(
                usuario=usuario,
                tipo_contenido=modelo,
                id_contenido=instance.id,
                titulo__exact=f"Nuevo {modelo} pendiente de aprobación"
            ).exists()
            
            if not notificacion_existente:
                try:
                    # Crear la notificación con select_for_update para evitar duplicados
                    Notificacion.objects.create(
                        usuario=usuario,
                        titulo=f"Nuevo {modelo} pendiente de aprobación",
                        mensaje=f"Se ha añadido un nuevo {modelo.lower()} '{nombre_elemento}' que requiere su aprobación.",
                        tipo_contenido=modelo,
                        id_contenido=instance.id
                    )
                    logger.info(f"Notificación creada para {usuario.username} sobre {modelo} {instance.id}")
                except Exception as e:
                    logger.error(f"Error creando notificación: {e}")
            else:
                logger.info(f"Notificación duplicada evitada para {usuario.username} sobre {modelo} {instance.id}")

def crear_notificacion_cambio_estado(modelo, instance, estado_anterior):
    """
    Crea notificaciones cuando cambia el estado de aprobación
    """
    if instance.aprobacion == estado_anterior:
        return
    
    # Solo notificar cambios a aprobado o rechazado
    if instance.aprobacion not in ['Aprobado', 'No Válido']:
        return
    
    # Usar transacción para evitar condiciones de carrera
    with transaction.atomic():
        # Determinar destinatarios (creador y colaboradores)
        destinatarios = []
        
        # Añadir el creador
        if hasattr(instance, 'usuario') and instance.usuario:
            destinatarios.append(instance.usuario)
        
        # Añadir colaboradores según el tipo
        if hasattr(instance, 'autores') and callable(instance.autores):
            if instance.autores().exists():
                destinatarios.extend(instance.autores())

        elif hasattr(instance, 'premiados') and callable(instance.premiados):
            if instance.premiados().exists():
                destinatarios.extend(instance.premiados())

        elif hasattr(instance, 'participantes') and callable(instance.participantes):
            if instance.participantes().exists():
                destinatarios.extend(instance.participantes())

        
        # Eliminar duplicados
        destinatarios = list(set(destinatarios))
        
        # Determinar el nombre del elemento
        nombre_elemento = ""
        if hasattr(instance, 'titulo'):
            nombre_elemento = instance.titulo
        elif hasattr(instance, 'nombre_proyecto'):
            nombre_elemento = instance.nombre_proyecto
        elif hasattr(instance, 'nombre_programa'):
            nombre_elemento = instance.nombre_programa
        else:
            nombre_elemento = str(instance)
        
        # Determinar el mensaje
        if instance.aprobacion == 'Aprobado':
            titulo = f"{modelo} aprobado"
            mensaje = f"Su {modelo.lower()} '{nombre_elemento}' ha sido aprobado."
        else:  # No Válido
            titulo = f"{modelo} rechazado"
            mensaje = f"Su {modelo.lower()} '{nombre_elemento}' ha sido rechazado."
        
        # Crear notificaciones evitando duplicados
        for usuario in destinatarios:
            # 👇 Validar que sea instancia de Usuario
            if not isinstance(usuario, Usuario):
                try:
                    usuario = Usuario.objects.get(username=usuario)
                except Usuario.DoesNotExist:
                    logger.warning(f"Usuario {usuario} no existe, se omite la notificación")
                    continue  # pasa al siguiente destinatario
            
            notificacion_existente = Notificacion.objects.filter(
                usuario=usuario,
                tipo_contenido=modelo,
                id_contenido=instance.id,
                titulo__exact=titulo
            ).exists()

            if not notificacion_existente:
                try:
                    Notificacion.objects.create(
                        usuario=usuario,
                        titulo=titulo,
                        mensaje=mensaje,
                        tipo_contenido=modelo,
                        id_contenido=instance.id
                    )
                    logger.info(f"Notificación de cambio de estado creada para {usuario.username}")
                except Exception as e:
                    logger.error(f"Error creando notificación de cambio de estado: {e}")
            else:
                logger.info(f"Notificación de cambio de estado duplicada evitada para {usuario.username}")

            
            if not notificacion_existente:
                try:
                    Notificacion.objects.create(
                        usuario=usuario,
                        titulo=titulo,
                        mensaje=mensaje,
                        tipo_contenido=modelo,
                        id_contenido=instance.id
                    )
                    logger.info(f"Notificación de cambio de estado creada para {usuario.username}")
                except Exception as e:
                    logger.error(f"Error creando notificación de cambio de estado: {e}")
            else:
                logger.info(f"Notificación de cambio de estado duplicada evitada para {usuario.username}")

# Signals para creación de elementos
@receiver(post_save, sender=Articulo)
def notificar_nuevo_articulo(sender, instance, created, **kwargs):
    if created and instance.aprobacion == 'Pendiente':
        # Usar transaction.on_commit para asegurar que la instancia esté guardada
        transaction.on_commit(lambda: crear_notificacion_sin_duplicados('Articulo', instance))

@receiver(post_save, sender=Evento)
def notificar_nuevo_evento(sender, instance, created, **kwargs):
    if created and instance.aprobacion == 'Pendiente':
        transaction.on_commit(lambda: crear_notificacion_sin_duplicados('Evento', instance))

@receiver(post_save, sender=Premio)
def notificar_nuevo_premio(sender, instance, created, **kwargs):
    if created and instance.aprobacion == 'Pendiente':
        transaction.on_commit(lambda: crear_notificacion_sin_duplicados('Premio', instance))

@receiver(post_save, sender=Proyecto)
def notificar_nuevo_proyecto(sender, instance, created, **kwargs):
    if created and instance.aprobacion == 'Pendiente':
        transaction.on_commit(lambda: crear_notificacion_sin_duplicados('Proyecto', instance))

@receiver(post_save, sender=Programa)
def notificar_nuevo_programa(sender, instance, created, **kwargs):
    if created and instance.aprobacion == 'Pendiente':
        transaction.on_commit(lambda: crear_notificacion_sin_duplicados('Programa', instance))

# Signals para cambios de estado
@receiver(pre_save, sender=Articulo)
def articulo_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._estado_anterior = Articulo.objects.get(pk=instance.pk).aprobacion
        except Articulo.DoesNotExist:
            instance._estado_anterior = None

@receiver(post_save, sender=Articulo)
def articulo_post_save(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_estado_anterior'):
        transaction.on_commit(lambda: crear_notificacion_cambio_estado('Articulo', instance, instance._estado_anterior))

@receiver(pre_save, sender=Evento)
def evento_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._estado_anterior = Evento.objects.get(pk=instance.pk).aprobacion
        except Evento.DoesNotExist:
            instance._estado_anterior = None

@receiver(post_save, sender=Evento)
def evento_post_save(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_estado_anterior'):
        transaction.on_commit(lambda: crear_notificacion_cambio_estado('Evento', instance, instance._estado_anterior))

@receiver(pre_save, sender=Premio)
def premio_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._estado_anterior = Premio.objects.get(pk=instance.pk).aprobacion
        except Premio.DoesNotExist:
            instance._estado_anterior = None

@receiver(post_save, sender=Premio)
def premio_post_save(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_estado_anterior'):
        transaction.on_commit(lambda: crear_notificacion_cambio_estado('Premio', instance, instance._estado_anterior))

@receiver(pre_save, sender=Proyecto)
def proyecto_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._estado_anterior = Proyecto.objects.get(pk=instance.pk).aprobacion
        except Proyecto.DoesNotExist:
            instance._estado_anterior = None

@receiver(post_save, sender=Proyecto)
def proyecto_post_save(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_estado_anterior'):
        transaction.on_commit(lambda: crear_notificacion_cambio_estado('Proyecto', instance, instance._estado_anterior))

@receiver(pre_save, sender=Programa)
def programa_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._estado_anterior = Programa.objects.get(pk=instance.pk).aprobacion
        except Programa.DoesNotExist:
            instance._estado_anterior = None

@receiver(post_save, sender=Programa)
def programa_post_save(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_estado_anterior'):
        transaction.on_commit(lambda: crear_notificacion_cambio_estado('Programa', instance, instance._estado_anterior))
