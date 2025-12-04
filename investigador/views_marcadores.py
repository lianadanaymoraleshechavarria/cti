from .forms import (Evento_Form, TipoPremioForm, CaracterPremioForm, Proyecto_Form, InstitucionForm, Programa_Form, Premio_Form, 
                    Perfil_Form, EventoBaseForm, Colaborador_Form, ArticuloForm)
from .models import (Evento, Proyecto, Programa, Premio, Perfil, Articulo, TipoEvento, Modalidad, TipoPremio, TipoParticipacion, ArticuloAutor,
                     Area, EntidadParticipante, Colaborador, EventoBase, PremioPremiado, Institucion, EventoAutor, Revista_Libro_Conferencia)
from .serializers import TipoParticipacionSerializer
from django.db.models import Count
import json
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from collections import defaultdict
from django.contrib import messages
from django.utils import timezone
from .choices import APROBACION 
from django.db import transaction
from django.http import Http404
from django.views import View
from itertools import chain
import datetime
from django.db.models import Case, When, Value, BooleanField, Q, F
import uuid
from django.db.models.functions import ExtractYear 
from django.db.models import CharField, IntegerField, DateField, Value
from django.urls import NoReverseMatch, reverse
from django.http import JsonResponse
from django.db.models import Q
from plataforma.models import Usuario
import logging
from django.core.paginator import Paginator
from .models import Notificacion
from plataforma.decorators import vicerrector_required, jefearea_required
from django.db.models import Q
from itertools import chain
from django.db.models import Q, Case, When, Value, BooleanField
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth import get_user_model
from plataforma.choices import PROVINCIAS_CUBA, PAIS, IDIOMA 
from django.http import HttpRequest, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings
import re
from rest_framework.views import APIView
from rest_framework.response import Response

# Configurar logging
logger = logging.getLogger(__name__)
Usuario = get_user_model()


@csrf_exempt  # si usas CSRF desde JS, no necesitas esto
def crear_entidad(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre")
            if not nombre:
                return JsonResponse({"error": "El nombre es requerido"}, status=400)
            entidad, created = EntidadParticipante.objects.get_or_create(
                nombre=nombre.strip().title(),
                defaults={
                    "sigla": data.get("sigla","").strip().upper(),
                    "tipo_entidad": data.get("tipo","Otro"),
                    "pais": data.get("pais","Cuba")
                }
            )
            return JsonResponse({"id": entidad.id, "nombre": str(entidad)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

class TipoParticipacionList(APIView):
    def get(self, request):
        term = request.GET.get('term', '').strip()
        qs = TipoParticipacion.objects.all()
        if term:
            qs = qs.filter(nombre__icontains=term)
        serializer = TipoParticipacionSerializer(qs, many=True)
        # Formato compatible con Select2
        data = [{'id': t['id'], 'text': t['nombre']} for t in serializer.data]
        return Response({'results': data})
    
    
def buscar_entidades(request):
    term = request.GET.get("term", "").strip()

    entidades = EntidadParticipante.objects.filter(
        nombre__icontains=term,
        activo=True
    ).order_by("nombre")

    resultados = [
        {"id": e.id, "text": e.nombre}
        for e in entidades
    ]

    # Si no existe → ofrecer crear nueva
    if term and not entidades.exists():
        resultados.append({
            "id": f"new-{term}",
            "text": f"➕ Crear '{term}'"
        })

    return JsonResponse({"results": resultados})


@login_required
def lista_notificaciones(request):
    """Vista mejorada para mostrar todas las notificaciones del usuario con paginación"""
    notificaciones_list = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(notificaciones_list, 10)  # 10 notificaciones por página
    page_number = request.GET.get('page')
    notificaciones = paginator.get_page(page_number)
    
    # Estadísticas
    total = notificaciones_list.count()
    no_leidas = notificaciones_list.filter(leida=False).count()
    
    context = {
        'notificaciones': notificaciones,
        'total': total,
        'no_leidas': no_leidas,
    }
    
    return render(request, 'notificaciones/lista_notificaciones.html', context)


@login_required
def eliminar_notificacion(request, notificacion_id):
    """Vista para eliminar una notificación específica"""
    if request.method == 'POST':
        try:
            notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
            notificacion.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Notificación eliminada correctamente'
            })
        except Exception as e:
            logger.error(f"Error eliminando notificación {notificacion_id}: {e}")
            return JsonResponse({
                'success': False,
                'message': 'Error al eliminar la notificación'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def eliminar_todas_notificaciones(request):
    """Vista para eliminar todas las notificaciones del usuario"""
    if request.method == 'POST':
        try:
            count = Notificacion.objects.filter(usuario=request.user).count()
            Notificacion.objects.filter(usuario=request.user).delete()
            
            return JsonResponse({
                'success': True,
                'message': f'{count} notificaciones eliminadas correctamente',
                'count': count
            })
        except Exception as e:
            logger.error(f"Error eliminando todas las notificaciones del usuario {request.user.id}: {e}")
            return JsonResponse({
                'success': False,
                'message': 'Error al eliminar las notificaciones'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """Vista mejorada para marcar una notificación como leída con respuesta AJAX"""
    if request.method == 'POST':
        try:
            notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
            notificacion.marcar_como_leida()
            
            return JsonResponse({
                'success': True,
                'message': 'Notificación marcada como leída'
            })
        except Exception as e:
            logger.error(f"Error marcando notificación {notificacion_id} como leída: {e}")
            return JsonResponse({
                'success': False,
                'message': 'Error al marcar como leída'
            })
    
    # Fallback para requests no AJAX
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.marcar_como_leida()
    return redirect('lista_notificaciones')


@login_required
def marcar_todas_leidas(request):
    """Vista mejorada para marcar todas las notificaciones como leídas"""
    if request.method == 'POST':
        try:
            count = Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
            
            # Si es una petición AJAX
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': f'{count} notificaciones marcadas como leídas',
                    'count': count
                })
            
            messages.success(request, f'{count} notificaciones marcadas como leídas')
        except Exception as e:
            logger.error(f"Error marcando todas las notificaciones como leídas: {e}")
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': 'Error al marcar las notificaciones'
                })
            messages.error(request, 'Error al marcar las notificaciones como leídas')
    
    return redirect('lista_notificaciones')


@login_required
def obtener_contador_notificaciones(request):
    """Vista para obtener el número de notificaciones no leídas (para AJAX)"""
    try:
        contador = Notificacion.objects.filter(usuario=request.user, leida=False).count()
        return JsonResponse({
            'contador': contador,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error obteniendo contador de notificaciones: {e}")
        return JsonResponse({
            'contador': 0,
            'success': False
        })


@login_required
def ver_notificacion(request, notificacion_id):
    """Vista mejorada para ver el detalle de una notificación y redirigir al elemento relacionado"""
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    
    # Marcar como leída
    notificacion.marcar_como_leida()
    
    # Obtener el rol del usuario
    rol_usuario = getattr(request.user, 'rol', 'Investigador')
    
    # Registrar información para depuración
    logger.info(f"Procesando notificación: ID={notificacion.id}, Tipo={notificacion.tipo_contenido}, ID_Contenido={notificacion.id_contenido}, Rol={rol_usuario}")
    
    # Verificar que id_contenido sea válido
    if not notificacion.id_contenido:
        messages.error(request, "La notificación no tiene un ID de contenido válido.")
        logger.error(f"Notificación {notificacion.id} no tiene ID de contenido válido")
        return redirect('lista_notificaciones')
    
    # Intentar diferentes formatos de nombres de URL
    tipo = notificacion.tipo_contenido
    
    # Lista de posibles patrones de URL basados en el rol
    patrones_url = []
    
    # Patrones específicos por rol
    if rol_usuario == 'Vicerrector':
        patrones_url.extend([
            f"{tipo}_Detail_Vicerrector",
            f"{tipo}_detail_Vicerrector",
            f"{tipo.lower()}_detail_vicerrector",
        ])
    elif rol_usuario == 'Jefe_area':
        patrones_url.extend([
            f"{tipo}_Detail_JefeArea",
            f"{tipo}_detail_JefeArea",
            f"{tipo.lower()}_detail_jefearea",
        ])
    elif rol_usuario == 'Jefe_departamento':
        patrones_url.extend([
            f"{tipo}_Detail_JefeDepartamento",
            f"{tipo}_detail_JefeDepartamento",
            f"{tipo.lower()}_detail_jefedepartamento",
        ])
    elif rol_usuario == 'Administrador':
        patrones_url.extend([
            f"{tipo}_Detail_Admin",
            f"{tipo}_detail_Admin",
            f"{tipo.lower()}_detail_admin",
        ])
    else:  # Investigador u otros roles
        patrones_url.extend([
            f"{tipo}_Detail_Investigador",
            f"{tipo}_detail_Investigador",
            f"{tipo.lower()}_detail_investigador",
        ])
    
    # Patrones genéricos como fallback
    patrones_url.extend([
        f"{tipo}_detail",
        f"{tipo.lower()}_detail",
        f"{tipo}_Detail",
        f"{tipo.lower()}_Detail",
    ])
    
    # Intentar cada patrón de URL
    for url_name in patrones_url:
        try:
            # Verificar si la URL existe
            url = reverse(url_name, kwargs={'pk': notificacion.id_contenido})
            logger.info(f"URL encontrada: {url_name} -> {url}")
            return redirect(url_name, pk=notificacion.id_contenido)
        except NoReverseMatch:
            logger.debug(f"URL no encontrada: {url_name}")
            continue
    
    # Si llegamos aquí, ninguna URL funcionó
    logger.warning(f"No se encontró ninguna URL válida para la notificación {notificacion.id}")
    messages.warning(request, f"No se pudo encontrar la página de detalles para este {tipo.lower()}. Contacte al administrador.")
    
    # Intentar redirigir a una vista de lista genérica como último recurso
    try:
        if rol_usuario == 'Vicerrector':
            list_url_name = f"{tipo}_List_Vicerrector"
        elif rol_usuario == 'Jefe_area':
            list_url_name = f"{tipo}_List_JefeArea"
        elif rol_usuario == 'Jefe_departamento':
            list_url_name = f"{tipo}_List_JefeDepartamento"
        elif rol_usuario == 'Administrador':
            list_url_name = f"{tipo}_List_Admin"
        else:
            list_url_name = f"{tipo}_List_Investigador"
        
        return redirect(list_url_name)
    except NoReverseMatch:
        # Si todo falla, volver a la lista de notificaciones
        return redirect('lista_notificaciones')


@login_required
def cambiar_estado_desde_notificacion(request, notificacion_id):
    """Vista para cambiar el estado de aprobación directamente desde una notificación"""
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    
    # Verificar permisos
    if not request.user.rol in ['Vicerrector', 'Jefe_area', 'Jefe_departamento', 'Administrador']:
        messages.error(request, 'No tiene permisos para cambiar estados de aprobación.')
        return redirect('lista_notificaciones')
    
    # Verificar que la notificación sea de un elemento pendiente
    if 'pendiente' not in notificacion.titulo.lower():
        messages.error(request, 'Esta notificación no corresponde a un elemento pendiente de aprobación.')
        return redirect('lista_notificaciones')
    
    # Obtener el modelo y la instancia
    tipo = notificacion.tipo_contenido
    modelo_map = {
        'Articulo': Articulo,
        'Evento': Evento,
        'Premio': Premio,
        'Proyecto': Proyecto,
        'Programa': Programa,
    }
    
    if tipo not in modelo_map:
        messages.error(request, f'Tipo de contenido no válido: {tipo}')
        return redirect('lista_notificaciones')
    
    modelo = modelo_map[tipo]
    
    try:
        instance = modelo.objects.get(id=notificacion.id_contenido)
    except modelo.DoesNotExist:
        messages.error(request, f'El {tipo.lower()} ya no existe.')
        return redirect('lista_notificaciones')
    
    # Verificar permisos específicos según el rol y área/departamento
    if request.user.rol == 'Jefe_area':
        if hasattr(instance, 'area') and instance.area != request.user.area:
            messages.error(request, 'No tiene permisos para aprobar elementos de otras áreas.')
            return redirect('lista_notificaciones')
    elif request.user.rol == 'Jefe_departamento':
        if hasattr(instance, 'departamento') and instance.departamento != request.user.departamento:
            messages.error(request, 'No tiene permisos para aprobar elementos de otros departamentos.')
            return redirect('lista_notificaciones')
    
    estados = ['Pendiente', 'Aprobado', 'No Válido']
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado not in estados:
            messages.error(request, 'Estado seleccionado no válido.')
            return redirect('cambiar_estado_desde_notificacion', notificacion_id=notificacion_id)
        
        # Guardar estado anterior para logging
        estado_anterior = instance.aprobacion
        
        # Cambiar el estado
        instance.aprobacion = nuevo_estado
        instance.save()
        
        # Marcar la notificación como leída
        notificacion.marcar_como_leida()
        
        # Mensaje de éxito
        messages.success(request, f'El estado del {tipo.lower()} ha sido cambiado a "{nuevo_estado}" exitosamente.')
        
        # Log del cambio
        logger.info(f"Usuario {request.user.username} cambió estado de {tipo} {instance.id} de '{estado_anterior}' a '{nuevo_estado}'")
        
        # Redirigir a la lista de notificaciones
        return redirect('lista_notificaciones')
    
    context = {
        'notificacion': notificacion,
        'instance': instance,
        'tipo': tipo,
        'estados': estados,
    }
    
    return render(request, 'notificaciones/cambiar_estado.html', context)


def notificar_cambio_estado(modelo, instance, estado_anterior):
    """
    Función auxiliar para notificar al creador y colaboradores cuando cambia el estado de aprobación
    
    Args:
        modelo: Nombre del modelo (Articulo, Evento, etc.)
        instance: Instancia del modelo que ha cambiado
        estado_anterior: Estado de aprobación anterior
    """
    # Si el estado no ha cambiado, no hacer nada
    if instance.aprobacion == estado_anterior:
        return
    
    # Solo notificar cambios a aprobado o rechazado
    if instance.aprobacion not in ['Aprobado', 'No Válido']:
        return
    
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
    
    # Determinar el mensaje según el nuevo estado
    if instance.aprobacion == 'Aprobado':
        titulo = f"{modelo} aprobado"
        mensaje = f"Su {modelo.lower()} '{nombre_elemento}' ha sido aprobado."
    else:  # No Válido
        titulo = f"{modelo} rechazado"
        mensaje = f"Su {modelo.lower()} '{nombre_elemento}' ha sido rechazado."
    
    # Lista de destinatarios (creador y colaboradores)
    destinatarios = []
    
    # Añadir el creador a los destinatarios
    if hasattr(instance, 'usuario') and instance.usuario:
        destinatarios.append(instance.usuario)
    
    # Añadir colaboradores/autores si existen
    if hasattr(instance, 'autores') and instance.autores.exists():
        destinatarios.extend(instance.autores.all())
    elif hasattr(instance, 'premiados') and instance.premiados.exists():
        destinatarios.extend(instance.premiados.all())
    elif hasattr(instance, 'participantes') and instance.participantes.exists():
        destinatarios.extend(instance.participantes.all())
    
    # Eliminar duplicados (por si el creador también está en colaboradores)
    destinatarios = list(set(destinatarios))
    
    # Crear notificaciones para cada destinatario evitando duplicados
    for usuario in destinatarios:
        # Verificar si ya existe una notificación similar
        notificacion_existente = Notificacion.objects.filter(
            usuario=usuario,
            tipo_contenido=modelo,
            id_contenido=instance.id,
            titulo=titulo
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


# Funciones auxiliares para las vistas de cambio de estado existentes
@login_required
def cambiar_estado_articulo_mejorado(request, id):
    """Vista mejorada para cambiar estado de artículo con notificaciones"""
    articulo = get_object_or_404(Articulo, pk=id)
    estado_anterior = articulo.aprobacion
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['Pendiente', 'No Válido', 'Aprobado']:
            articulo.aprobacion = nuevo_estado
            articulo.save()
            
            # Notificar cambio de estado
            notificar_cambio_estado('Articulo', articulo, estado_anterior)
            
            messages.success(request, f'El estado del artículo ha sido cambiado a {nuevo_estado}')
            return redirect('Articulo_List_JefeArea')
    
    estados = ['Pendiente', 'No Válido', 'Aprobado']
    return render(request, "JefeArea/Articulo/cambiar_estado_articulo.html", {
        'estados': estados,
        'articulo': articulo
    })


@login_required
def cambiar_estado_proyecto_mejorado(request, id):
    """Vista mejorada para cambiar estado de proyecto con notificaciones"""
    proyecto = get_object_or_404(Proyecto, pk=id)
    estado_anterior = proyecto.aprobacion
    
    if request.method == 'POST':
        proyecto.aprobacion = request.POST['estado']
        proyecto.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Proyecto', proyecto, estado_anterior)
        
        messages.success(request, 'El estado del proyecto ha sido actualizado con éxito.')
        return redirect('Proyecto_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Proyecto/cambiar_estado_proyecto.html", {
            'estados': estados,
            'proyecto': proyecto
        })


@login_required
def cambiar_estado_programa_mejorado(request, id):
    """Vista mejorada para cambiar estado de programa con notificaciones"""
    programa = get_object_or_404(Programa, pk=id)
    estado_anterior = programa.aprobacion
    
    if request.method == 'POST':
        programa.aprobacion = request.POST['estado']
        programa.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Programa', programa, estado_anterior)
        
        messages.success(request, 'El estado del programa ha sido actualizado con éxito.')
        return redirect('Programa_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Programa/cambiar_estado_programa.html", {
            'estados': estados,
            'programa': programa
        })


@login_required
def cambiar_estado_premio_mejorado(request, id):
    """Vista mejorada para cambiar estado de premio con notificaciones"""
    premio = get_object_or_404(Premio, pk=id)
    estado_anterior = premio.aprobacion
    
    if request.method == 'POST':
        premio.aprobacion = request.POST['estado']
        premio.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Premio', premio, estado_anterior)
        
        messages.success(request, 'El estado del premio ha sido actualizado con éxito.')
        return redirect('Premio_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Premio/cambiar_estado_premio.html", {
            'estados': estados,
            'premio': premio
        })


@login_required
def cambiar_estado_evento_mejorado(request, id):
    """Vista mejorada para cambiar estado de evento con notificaciones"""
    evento = get_object_or_404(Evento, pk=id)
    estado_anterior = evento.aprobacion
    
    if request.method == 'POST':
        evento.aprobacion = request.POST['estado']
        evento.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Evento', evento, estado_anterior)
        
        messages.success(request, 'El estado del evento ha sido actualizado con éxito.')
        return redirect('Evento_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Evento/cambiar_estado_evento.html", {
            'estados': estados,
            'evento': evento
        })


# Funciones auxiliares para las vistas de cambio de estado existentes
@login_required
def cambiar_estado_articulo_mejorado(request, id):
    """Vista mejorada para cambiar estado de artículo con notificaciones"""
    articulo = get_object_or_404(Articulo, pk=id)
    estado_anterior = articulo.aprobacion
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['Pendiente', 'No Válido', 'Aprobado']:
            articulo.aprobacion = nuevo_estado
            articulo.save()
            
            # Notificar cambio de estado
            notificar_cambio_estado('Articulo', articulo, estado_anterior)
            
            messages.success(request, f'El estado del artículo ha sido cambiado a {nuevo_estado}')
            return redirect('Articulo_List_JefeArea')
    
    estados = ['Pendiente', 'No Válido', 'Aprobado']
    return render(request, "JefeArea/Articulo/cambiar_estado_articulo.html", {
        'estados': estados,
        'articulo': articulo
    })


@login_required
def cambiar_estado_proyecto_mejorado(request, id):
    """Vista mejorada para cambiar estado de proyecto con notificaciones"""
    proyecto = get_object_or_404(Proyecto, pk=id)
    estado_anterior = proyecto.aprobacion
    
    if request.method == 'POST':
        proyecto.aprobacion = request.POST['estado']
        proyecto.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Proyecto', proyecto, estado_anterior)
        
        messages.success(request, 'El estado del proyecto ha sido actualizado con éxito.')
        return redirect('Proyecto_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Proyecto/cambiar_estado_proyecto.html", {
            'estados': estados,
            'proyecto': proyecto
        })


@login_required
def cambiar_estado_programa_mejorado(request, id):
    """Vista mejorada para cambiar estado de programa con notificaciones"""
    programa = get_object_or_404(Programa, pk=id)
    estado_anterior = programa.aprobacion
    
    if request.method == 'POST':
        programa.aprobacion = request.POST['estado']
        programa.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Programa', programa, estado_anterior)
        
        messages.success(request, 'El estado del programa ha sido actualizado con éxito.')
        return redirect('Programa_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Programa/cambiar_estado_programa.html", {
            'estados': estados,
            'programa': programa
        })


@login_required
def cambiar_estado_premio_mejorado(request, id):
    """Vista mejorada para cambiar estado de premio con notificaciones"""
    premio = get_object_or_404(Premio, pk=id)
    estado_anterior = premio.aprobacion
    
    if request.method == 'POST':
        premio.aprobacion = request.POST['estado']
        premio.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Premio', premio, estado_anterior)
        
        messages.success(request, 'El estado del premio ha sido actualizado con éxito.')
        return redirect('Premio_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Premio/cambiar_estado_premio.html", {
            'estados': estados,
            'premio': premio
        })


@login_required
def cambiar_estado_evento_mejorado(request, id):
    """Vista mejorada para cambiar estado de evento con notificaciones"""
    evento = get_object_or_404(Evento, pk=id)
    estado_anterior = evento.aprobacion
    
    if request.method == 'POST':
        evento.aprobacion = request.POST['estado']
        evento.save()
        
        # Notificar cambio de estado
        notificar_cambio_estado('Evento', evento, estado_anterior)
        
        messages.success(request, 'El estado del evento ha sido actualizado con éxito.')
        return redirect('Evento_List_JefeArea')
    else:
        estados = ['Pendiente', 'No Válido', 'Aprobado']
        return render(request, "JefeArea/Evento/cambiar_estado_evento.html", {
            'estados': estados,
            'evento': evento
        })


def api_usuarios(request):
    """API para buscar usuarios registrados y colaboradores externos"""
    search = request.GET.get('search', '')
    
    # Determinar el tipo de búsqueda (opcional)
    tipo = request.GET.get('tipo', 'todos')  # valores posibles: 'todos', 'usuarios', 'colaboradores'
    
    resultados = []
    
    # Buscar usuarios si el tipo es 'todos' o 'usuarios'
    if tipo in ['todos', 'usuarios']:
        usuarios = Usuario.objects.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) | 
            Q(username__icontains=search) |
            Q(carnet__icontains=search),
        ).select_related('area', 'departamento')[:15]  # Limitar a 15 resultados
        
        for usuario in usuarios:
            nombre_completo = usuario.get_full_name() or usuario.username
            
            # Información adicional
            info_adicional = []
            if usuario.carnet:
                info_adicional.append(f"Carnet: {usuario.carnet}")
            if usuario.area:
                info_adicional.append(f"Área: {usuario.area}")
            if usuario.departamento:
                info_adicional.append(f"Depto: {usuario.departamento}")
            
            # Rol del usuario
            rol = usuario.get_rol_display() if hasattr(usuario, 'get_rol_display') else ''
            
            # Construir el nombre para mostrar
            display_name = f"{nombre_completo} ({usuario.username})"
            if rol:
                display_name += f" - {rol}"
            
            resultados.append({
                'id': usuario.id,
                'tipo': 'usuario',
                'username': usuario.username,
                'name': display_name,
                'full_name': nombre_completo,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'carnet': usuario.carnet or '',
                'rol': rol,
                'area': str(usuario.area) if usuario.area else '',
                'departamento': str(usuario.departamento) if usuario.departamento else '',
                'info_adicional': info_adicional
            })
    
    # Buscar colaboradores si el tipo es 'todos' o 'colaboradores'
    if tipo in ['todos', 'colaboradores']:
        colaboradores = Colaborador.objects.filter(
            Q(nombre__icontains=search) | 
            Q(apellidos__icontains=search) |
            Q(orci__icontains=search),
            usuario=request.user
        )[:15]  # Limitar a 15 resultados
        
        for colaborador in colaboradores:
            nombre_completo = f"{colaborador.nombre} {colaborador.apellidos}"
            
            # Información adicional
            info_adicional = []
            if colaborador.orci:
                info_adicional.append(f"ORCID: {colaborador.orci}")
            
            # Construir el nombre para mostrar
            display_name = nombre_completo
            if colaborador.orci:
                display_name += f" (ORCID: {colaborador.orci})"
            
            resultados.append({
                'id': colaborador.id,
                'tipo': 'colaborador',
                'name': display_name,
                'full_name': nombre_completo,
                'first_name': colaborador.nombre,
                'last_name': colaborador.apellidos,
                'orci': colaborador.orci or '',
                'google_academico': colaborador.google_academico or '',
                'rgate': colaborador.rgate or '',
                'info_adicional': info_adicional
            })
    
    # Ordenar resultados por relevancia (primero usuarios, luego colaboradores)
    # y dentro de cada tipo por nombre completo
    resultados_ordenados = sorted(
        resultados, 
        key=lambda x: (0 if x['tipo'] == 'usuario' else 1, x['full_name'])
    )
    
    # Devolver resultados como JSON
    return JsonResponse(resultados_ordenados, safe=False)    


def obtener_institucion_tipo_premio(request, tipo_id):
    try:
        tipo = TipoPremio.objects.get(id=tipo_id)
        return JsonResponse({
            'institucion_id': tipo.institucion.id,
            'institucion_nombre': tipo.institucion.nombre
        })
    except TipoPremio.DoesNotExist:
        return JsonResponse({'error': 'Tipo no encontrado'}, status=404)
    
    
def tipo_premio_create_ajax(request):
    if request.method == "POST":
        form = TipoPremioForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            return JsonResponse({
                "success": True,
                "id": tipo.id,
                "nombre": tipo.nombre,
                "institucion_id": tipo.institucion.id,
                "institucion_nombre": tipo.institucion.nombre,
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors})
        

def api_tipos_premio(request):
    tipos = list(TipoPremio.objects.all().values('id', 'nombre'))
    return JsonResponse(tipos, safe=False)


def crear_institucion_ajax(request):
    if request.method == 'POST':
        form = InstitucionForm(request.POST)
        if form.is_valid():
            institucion = form.save()
            return JsonResponse({
                'success': True,
                'id': institucion.id,
                'nombre': institucion.nombre  # Solo se devuelven campos serializables
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)


@require_POST
def crear_caracter_premio(request):
    if request.method == 'POST':
        form = CaracterPremioForm(request.POST)
        if form.is_valid():
            caracter = form.save()
            return JsonResponse({
                'success': True,
                'id': caracter.id,
                'nombre': str(caracter)
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

import logging
logger = logging.getLogger(__name__)

@login_required
@require_POST
def crear_colaborador_ajax(request):
    form = Colaborador_Form(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    nombre = form.cleaned_data['nombre'].strip()
    apellidos = form.cleaned_data['apellidos'].strip()
    orci = (form.cleaned_data.get('orci') or '').strip()

    # evitar duplicados para este usuario
    if Colaborador.objects.filter(
        nombre__iexact=nombre,
        apellidos__iexact=apellidos,
        orci__iexact=orci,
        usuario=request.user
    ).exists():
        return JsonResponse({
            'success': False,
            'error': 'Ya existe un colaborador con ese nombre y apellidos para tu cuenta.'
        }, status=400)

    # guardar asignando el usuario creador
    colaborador = form.save(commit=False)
    colaborador.usuario = request.user
    colaborador.save()

    # si el form tuviera m2m:
    try:
        form.save_m2m()
    except Exception:
        pass

    return JsonResponse({
        'success': True,
        'id': colaborador.id,
        'nombre': f"{colaborador.nombre} {colaborador.apellidos}"
    })

#......................Dashboard.................................
class Dashboard_Investigador(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_investigador.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        # Optimización: Usamos annotate para reducir consultas a la base de datos
        estados = dict(APROBACION)
        totales_por_estado = defaultdict(lambda: {
            'articulos': 0, 
            'premios': 0, 
            'proyectos': 0, 
            'eventos': 0,  
            'programas': 0
        })

        # Consultas optimizadas para cada modelo
        def contar_por_estado(modelo, campo):
            return (
                modelo.objects
                .filter(usuario=usuario)
                .values(campo)
                .annotate(total=Count('id'))
                .order_by(campo)
            )

        # Procesar cada tipo de objeto
        for articulo in contar_por_estado(Articulo, 'aprobacion'):
            estado = estados.get(articulo['aprobacion'], 'No Válido')
            totales_por_estado[estado]['articulos'] += articulo['total']

        for premio in contar_por_estado(Premio, 'aprobacion'):
            estado = estados.get(premio['aprobacion'], 'No Válido')
            totales_por_estado[estado]['premios'] += premio['total']

        for proyecto in contar_por_estado(Proyecto, 'aprobacion'):
            estado = estados.get(proyecto['aprobacion'], 'No Válido')
            totales_por_estado[estado]['proyectos'] += proyecto['total']

        for evento in contar_por_estado(Evento, 'aprobacion'):
            estado = estados.get(evento['aprobacion'], 'No Válido')
            totales_por_estado[estado]['eventos'] += evento['total']

        for programa in contar_por_estado(Programa, 'aprobacion'):
            estado = estados.get(programa['aprobacion'], 'No Válido')
            totales_por_estado[estado]['programas'] += programa['total']

        # Datos para gráfica de estados
        data_grafica_estados = [{
            'nombre': estado,
            'valor': sum(totales.values())
        } for estado, totales in totales_por_estado.items()]

        # Datos para gráfica de pastel
        data_grafica_pie = [{
            'name': 'Artículos',
            'y': sum(estado['articulos'] for estado in totales_por_estado.values())
        }, {
            'name': 'Premios',
            'y': sum(estado['premios'] for estado in totales_por_estado.values())
        }, {
            'name': 'Proyectos',
            'y': sum(estado['proyectos'] for estado in totales_por_estado.values())
        }, {
            'name': 'Eventos',
            'y': sum(estado['eventos'] for estado in totales_por_estado.values())
        }, {
            'name': 'Programas',
            'y': sum(estado['programas'] for estado in totales_por_estado.values())
        }]

        # Datos anuales optimizados
        this_year = timezone.now().year
        user_creation_year = usuario.date_joined.year
        years = list(range(user_creation_year, this_year + 1))

        def contar_por_año(modelo):
            return (
                modelo.objects
                .filter(usuario=usuario)
                .values('fecha_create__year')
                .annotate(total=Count('id'))
                .order_by('fecha_create__year')
            )

        # Mapear resultados por año para cada modelo
        def mapear_por_año(queryset):
            resultados = {item['fecha_create__year']: item['total'] for item in queryset}
            return [resultados.get(year, 0) for year in years]

        data_for_chart = {
            'years': years,
            'programas': mapear_por_año(contar_por_año(Programa)),
            'eventos': mapear_por_año(contar_por_año(Evento)),
            'articulos': mapear_por_año(contar_por_año(Articulo)),
            'premios': mapear_por_año(contar_por_año(Premio)),
            'proyectos': mapear_por_año(contar_por_año(Proyecto)),
        }

        context.update({
            'data_for_chart': data_for_chart,
            'data_grafica_estados': data_grafica_estados,
            'data_grafica_pie': data_grafica_pie,
            'total_articulos': sum(item['y'] for item in data_grafica_pie if item['name'] == 'Artículos'),
            'total_premios': sum(item['y'] for item in data_grafica_pie if item['name'] == 'Premios'),
            'total_proyectos': sum(item['y'] for item in data_grafica_pie if item['name'] == 'Proyectos'),
            'total_eventos': sum(item['y'] for item in data_grafica_pie if item['name'] == 'Eventos'),
            'total_programas': sum(item['y'] for item in data_grafica_pie if item['name'] == 'Programas'),
        })

        return context#.......................Evento....................................


# Vistas para EventoBase
class EventoBaseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = EventoBase
    template_name = 'configuracion/evento_base_list.html'
    context_object_name = 'eventos_base'
    
    def test_func(self):
        # Solo administradores pueden acceder
        return self.request.user.is_staff


class EventoBaseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EventoBase
    form_class = EventoBaseForm
    template_name = 'configuracion/evento_base_form.html'
    success_url = reverse_lazy('evento_base_list')
    
    def test_func(self):
        # Solo administradores pueden acceder
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Evento base creado correctamente.')
        return super().form_valid(form)


class EventoBaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EventoBase
    form_class = EventoBaseForm
    template_name = 'configuracion/evento_base_form.html'
    success_url = reverse_lazy('evento_base_list')
    
    def test_func(self):
        # Solo administradores pueden acceder
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Evento base actualizado correctamente.')
        return super().form_valid(form)


class EventoBaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EventoBase
    template_name = 'configuracion/evento_base_confirm_delete.html'
    success_url = reverse_lazy('evento_base_list')
    
    def test_func(self):
        # Solo administradores pueden acceder
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Evento base eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


# API para autocompletado de eventos base
@login_required
def api_eventos_base(request):
    try:
        query = request.GET.get('search', '').strip()
        eventos = EventoBase.objects.all()

        if query:
            eventos = eventos.filter(titulo__icontains=query)

        data = [
            {
                'id': e.id,
                'titulo': e.titulo,
                'tipo': e.tipo.nombre if e.tipo else None,
                'institucion': e.institucion.nombre if e.institucion else None,
                'pais': e.pais,
                'provincia': e.provincia,
            }
            for e in eventos
        ]

        return JsonResponse(data, safe=False)

    except Exception as ex:
        import traceback
        print("ERROR en api_eventos_base:", traceback.format_exc())
        return JsonResponse({'error': str(ex)}, status=500)


@login_required
def api_crear_evento_base(request):
    if request.method == 'POST':
        data = {
            'titulo': request.POST.get('titulo'),
            'tipo_id': request.POST.get('tipo'),
            'institucion': request.POST.get('institucion'),
            'pais': request.POST.get('pais'),
            'provincia': request.POST.get('provincia') if request.POST.get('pais', '').lower() == 'cuba' else None,
        }
        
        # Validar datos
        required_fields = ['titulo', 'tipo_id', 'institucion', 'pais']
        missing_fields = [field for field in required_fields if not data[field]]
        
        if missing_fields:
            return JsonResponse({
                'success': False, 
                'errors': {'general': ['Los siguientes campos son requeridos: ' + ', '.join(missing_fields)]}
            })
        
        # Validación específica para Cuba
        if data['pais'].lower() == 'cuba':
            if not data['provincia']:
                return JsonResponse({
                    'success': False, 
                    'errors': {
                        'provincia': ['La provincia es requerida para eventos en Cuba'],
                        'provincias_disponibles': PROVINCIAS_CUBA  # Envía las provincias disponibles
                    }
                })
            
            # Verificar que la provincia seleccionada sea válida
            provincias_validas = [p[0] for p in PROVINCIAS_CUBA]
            if data['provincia'] not in provincias_validas:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'provincia': ['Provincia no válida para Cuba'],
                        'provincias_validas': provincias_validas
                    }
                })
        
        # Obtener las instancias
        tipo_evento = get_object_or_404(TipoEvento, id=data['tipo_id'])

        # Crear el evento base
        

        try:
            institucion = get_object_or_404(Institucion, id=data['institucion'])
            
            evento_base = EventoBase.objects.create(
                titulo=data['titulo'],
                tipo=tipo_evento,
                institucion=institucion,
                pais=data['pais'],
                provincia=data['provincia']
            )
            
            return JsonResponse({
                'success': True,
                'evento_base': {
                    'id': evento_base.id,
                    'titulo': evento_base.titulo,
                    'tipo': evento_base.tipo.id,
                    'tipo_nombre': str(evento_base.tipo),
                    'institucion': evento_base.institucion.id,
                    'pais': evento_base.pais,
                    'provincia': evento_base.provincia,
                },
                'provincias_cuba': PROVINCIAS_CUBA  # Opcional: devolver las provincias en la respuesta exitosa
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'errors': {'general': [str(e)]},
                'provincias_cuba': PROVINCIAS_CUBA  # Devuelve las provincias incluso en caso de error
            })
    
    # Para GET requests, puedes devolver las provincias disponibles
    elif request.method == 'GET':
        return JsonResponse({
            'provincias_cuba': PROVINCIAS_CUBA,
            'message': 'Lista de provincias de Cuba disponibles'
        })


@login_required
def api_crear_colaborador(request):
    if request.method == 'POST':
        try:
            # Extrae y valida datos del POST
            nombre = request.POST.get('nombre', '').strip()
            apellidos = request.POST.get('apellidos', '').strip()
            orci = request.POST.get('orci', '').strip()
            google_academico = request.POST.get('google_academico', '').strip()
            rgate = request.POST.get('rgate', '').strip()
            
            # Validaciones básicas
            errors = {}
            if not nombre:
                errors['nombre'] = 'El nombre es obligatorio'
            elif len(nombre) > 50:
                errors['nombre'] = 'El nombre no puede exceder 50 caracteres'
                
            if not apellidos:
                errors['apellidos'] = 'Los apellidos son obligatorios'
            elif len(apellidos) > 50:
                errors['apellidos'] = 'Los apellidos no pueden exceder 50 caracteres'
                
            if orci and len(orci) > 10:
                errors['orci'] = 'ORCI no puede exceder 10 caracteres'
                
            # Validación de URLs si se proporcionan
            if google_academico and not google_academico.startswith(('http://', 'https://')):
                errors['google_academico'] = 'Debe ser una URL válida'
                
            if rgate and not rgate.startswith(('http://', 'https://')):
                errors['rgate'] = 'Debe ser una URL válida'
                
            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            
            # Verificar si ya existe un colaborador con el mismo nombre y apellidos
            if Colaborador.objects.filter(nombre__iexact=nombre, apellidos__iexact=apellidos).exists():
                return JsonResponse({
                    'success': False,
                    'errors': 'Ya existe un colaborador con este nombre y apellidos'
                }, status=400)
            
            # Crear el colaborador
            colaborador = Colaborador.objects.create(
                nombre=nombre,
                apellidos=apellidos,
                orci=orci if orci else None,  # Guarda como NULL si está vacío
                google_academico=google_academico if google_academico else '',
                rgate=rgate if rgate else '',
                usuario=request.user
            )
            
            return JsonResponse({
                'success': True,
                'colaborador': {
                    'id': colaborador.id,
                    'nombre': colaborador.nombre,
                    'apellidos': colaborador.apellidos,
                    'orci': colaborador.orci,
                    'google_academico': colaborador.google_academico,
                    'rgate': colaborador.rgate,
                }
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': 'Error interno del servidor',
                'debug': str(e)  # Solo en desarrollo, quitar en producción
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)       


@login_required
def api_crear_revista_libro(request):
    response_data = {
        'success': False,
        'errors': {},
        'revista_libro': None
    }

    # Extraer y limpiar datos
    data = {k: v.strip() if isinstance(v, str) else v for k, v in request.POST.items()}

    # Validar campos obligatorios
    required_fields = ['titulo', 'editorial']
    for field in required_fields:
        if not data.get(field):
            response_data['errors'][field] = "Este campo es obligatorio"

    # Validar longitud de campos
    field_constraints = {
        'titulo': 200,
        'editorial': 200,
        'issn': 9,
        'isbn': 13,
        'pais': 50,
        'url': 200
    }

    for field, max_length in field_constraints.items():
        value = data.get(field, '')
        if value and len(value) > max_length:
            response_data['errors'][field] = f"Máximo {max_length} caracteres permitidos"

    # Validar formato ISSN
    issn = data.get('issn', '')
    if issn:
        if len(issn) != 9:
            response_data['errors']['issn'] = "ISSN debe tener exactamente 9 caracteres (incluyendo guión si aplica)"
        elif not re.match(r'^[0-9A-Za-z-]+$', issn):
            response_data['errors']['issn'] = "ISSN solo puede contener letras, números y guiones"
        
    # Validar formato ISBN
    isbn = data.get('isbn', '')
    if isbn:
        if not isbn.isdigit():
            response_data['errors']['isbn'] = "ISBN debe contener solo números"
        elif len(isbn) not in [10, 13]:
            response_data['errors']['isbn'] = "ISBN debe tener 10 o 13 dígitos"

    # Validar URL
    url = data.get('url', '')
    if url and not url.startswith(('http://', 'https://')):
        response_data['errors']['url'] = "URL debe comenzar con http:// o https://"

    # Retornar errores si existen
    if response_data['errors']:
        return JsonResponse(response_data, status=400)

    try:
        # Crear registro
        revista_libro = Revista_Libro_Conferencia(
            titulo=data['titulo'],
            editorial=data['editorial'],
            issn=issn or None,
            isbn=isbn or None,
            pais=data.get('pais') or None,
            url=url or None,
            usuario=request.user
        )

        revista_libro.full_clean()  # Validación Django
        revista_libro.save()

        response_data.update({
            'success': True,
            'revista_libro': {
                'id': revista_libro.id,
                'titulo': revista_libro.titulo,
                'editorial': revista_libro.editorial,
                'issn': revista_libro.issn,
                'isbn': revista_libro.isbn,
                'pais': revista_libro.pais,
                'url': revista_libro.url
            }
        })

        return JsonResponse(response_data, status=201)

    except ValidationError as e:
        response_data['errors'] = e.message_dict
        return JsonResponse(response_data, status=400)

    except IntegrityError:
        response_data['errors']['non_field'] = "Error de base de datos. Posible duplicado."
        return JsonResponse(response_data, status=400)

    except Exception as e:
        response_data['errors']['non_field'] = "Error interno del servidor"
        if getattr(settings, 'DEBUG', False):
            response_data['debug'] = str(e)
        return JsonResponse(response_data, status=500)

class Evento_Create(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = Evento_Form
    template_name = 'Evento/evento_Create.html'
    success_url = reverse_lazy('Evento_List_Investigador')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['proyectos'] = Proyecto.objects.filter(aprobacion='Aprobado')
        context['instituciones'] = Institucion.objects.all()
        return context    

    def form_valid(self, form):
        user = self.request.user
        form.instance.usuario = user
        form.instance.area = user.area
        form.instance.departamento = user.departamento

        if not form.instance.titulo:
            form.instance.titulo = "Evento sin título"

        if not form.cleaned_data.get("evento_base"):
            form.instance.evento_base = EventoBase.objects.create(
                titulo=form.cleaned_data["titulo"],
                tipo=form.cleaned_data.get("tipo"),
                institucion=form.cleaned_data.get("institucion"),
                pais=form.cleaned_data.get("pais"),
                provincia=form.cleaned_data.get("provincia"),
            )

        response = super().form_valid(form)
        evento = self.object

        EventoAutor.objects.create(evento=evento, usuario=user)

        for seleccionado in form.cleaned_data.get('autores', []):
            try:
                tipo, id_str = seleccionado.split('-', 1)
            except ValueError:
                tipo, id_str = 'usuario', seleccionado

            if tipo == 'usuario':
                usuario = Usuario.objects.filter(id=int(id_str)).first()
                if usuario and usuario.id != user.id:
                    EventoAutor.objects.get_or_create(evento=evento, usuario=usuario)
            elif tipo == 'colaborador':
                colaborador = Colaborador.objects.filter(id=int(id_str)).first()
                if colaborador:
                    EventoAutor.objects.get_or_create(evento=evento, colaborador=colaborador)

        messages.success(self.request, "Evento creado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, f"Errores en el formulario: {form.errors.as_json()}")
        return super().form_invalid(form)

    
class Evento_List_Investigador(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "Evento/evento_list_investigador.html" 
    context_object_name = 'eventos'

    def get_queryset(self):
        user = self.request.user
        return Evento.objects.filter(usuario=user).distinct().annotate(
            es_creador=Case(
                When(usuario=user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seccion_actual'] = 'eventos'
        
        eventos = context['eventos']
        for e in eventos:
            autores = list(e.autores())
            if e.usuario in autores:
                e.contador_autores = len(autores)
            else:
                e.contador_autores = len(autores) 
        return context
    
    
class Evento_Detail_Investigador(LoginRequiredMixin, DetailView):
    model = Evento
    template_name =  "Evento/evento_detail_investigador.html" 
    context_object_name = 'evento'

    def get_queryset(self):
        return Evento.objects.filter(usuario=self.request.user)


def Evento_Delete_Investigador(request,id):
    evento = Evento.objects.get(id=id)
    evento.delete()
    return redirect("Evento_List_Investigador")


def Evento_Update_Investigador(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    autores_choices = []
    autores_initial = []
    for ea in EventoAutor.objects.filter(evento=evento).select_related('usuario','colaborador'):
        if ea.usuario_id:
            key = f'usuario-{ea.usuario_id}'
            label = ea.usuario.get_full_name() or ea.usuario.username
        else:
            key = f'colaborador-{ea.colaborador_id}'
            label = f'{(ea.colaborador.nombre or "").strip()} {(ea.colaborador.apellidos or "").strip()}'.strip()
        autores_choices.append((key, label))
        autores_initial.append(key)

    if request.method == 'POST':
        form = Evento_Form(
            request.POST,
            request.FILES,   
            instance=evento,
            user=request.user,
            initial={'autores': autores_initial},
        )
        form.fields['autores'].choices = autores_choices

        if form.is_valid():
            evento = form.save(commit=False)
            evento.save()

            nuevos_autores = form.cleaned_data.get('autores', [])

            ids_usuarios = [int(a.split('-')[1]) for a in nuevos_autores if a.startswith('usuario-')]
            ids_colaboradores = [int(a.split('-')[1]) for a in nuevos_autores if a.startswith('colaborador-')]

            EventoAutor.objects.filter(evento=evento).exclude(
                Q(usuario__id__in=ids_usuarios) | Q(colaborador__id__in=ids_colaboradores)
            ).delete()

            for a in nuevos_autores:
                tipo, id_str = a.split('-')
                if tipo == 'usuario':
                    usuario = Usuario.objects.get(id=int(id_str))
                    EventoAutor.objects.get_or_create(evento=evento, usuario=usuario)
                elif tipo == 'colaborador':
                    colaborador = Colaborador.objects.get(id=int(id_str))
                    EventoAutor.objects.get_or_create(evento=evento, colaborador=colaborador)

            if not EventoAutor.objects.filter(evento=evento, usuario=request.user).exists():
                EventoAutor.objects.create(evento=evento, usuario=request.user)

            return redirect(reverse('Evento_List_Investigador'))  

    else:
        form = Evento_Form(
            instance=evento,
            user=request.user,
            initial={'autores': autores_initial},
        )
        form.fields['autores'].choices = autores_choices

    proyectos = Proyecto.objects.filter(aprobacion='Aprobado')
    return render(request, 'Evento/evento_update_investigador.html', {'form': form, 'proyectos': proyectos})

#................................Proyecto..................................

def generar_codigo_unico():
    date_part = datetime.datetime.now().strftime('%Y%m%d')
    short_date_part = date_part[:4]
    potential_unique_id = f"{short_date_part}-{uuid.uuid4().hex[:8]}"
    
    while Proyecto.objects.filter(codigo_proyecto=potential_unique_id).exists() or Programa.objects.filter(codigo_programa=potential_unique_id).exists():
        short_date_part = datetime.datetime.now().strftime('%Y%m%d')[:4]
        potential_unique_id = f"{short_date_part}-{uuid.uuid4().hex[:8]}"
    return potential_unique_id 


class Proyecto_Create(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = Proyecto_Form
    template_name = "Proyecto/proyecto_create.html"
    success_url = reverse_lazy('Proyecto_Create')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el Proyecto. Por favor, intenta de nuevo.")
        print(form.errors)  # Esto imprimirá los errores en la consola del servidor
        return super().form_invalid(form)  

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.codigo_proyecto = generar_codigo_unico()
        messages.success(self.request, "Proyecto creado exitosamente.")
        return super().form_valid(form)
   
    
class Proyecto_List_Investigador(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name =  "Proyecto/proyecto_list_investigador.html" 
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


class Proyecto_Detail_Investigador(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name =  "Proyecto/proyecto_detail_investigador.html" 
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


def Proyecto_Delete_Investigador(request,id):
    proyecto = Proyecto.objects.get(id=id)
    proyecto.delete()
    return redirect("Proyecto_List_Investigador")


def Proyecto_Update_Investigador(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    if request.method == 'POST':
        form = Proyecto_Form(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
        return redirect('Proyecto_List_Investigador')
    else:
        form = Proyecto_Form(instance=proyecto)  
        return render(request, 'Proyecto/proyecto_update_investigador.html', {'form': form})
    

#................................Programa..................................

class Programa_Create(LoginRequiredMixin, CreateView):
    model = Programa
    form_class = Programa_Form
    template_name = "Programa/programa_create.html"
    success_url = reverse_lazy('Programa_List_Vicerrector')

    def form_invalid(self, form):
    # Agregar errores de campos individuales
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, error)  # Error general
                else:
                    # Error de campo específico
                    messages.error(self.request, f"{form.fields[field].label}: {error}")
        return super().form_invalid(form)
        

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Programa creado exitosamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["TIPOS_ENTIDAD"] = EntidadParticipante.TIPOS_ENTIDAD
        context['request'] = self.request
        # Agregar los proyectos aprobados al contexto
        context['proyectos'] = Proyecto.objects.filter(aprobacion='Aprobado')
        return context    

    
class Programa_List_Investigador(LoginRequiredMixin, ListView):
    model = Programa
    template_name =  "Programa/programa_list_investigador.html" 
    context_object_name = 'programa'

    def get_queryset(self):
        return Programa.objects.filter(usuario=self.request.user)


class Programa_Detail_Investigador(LoginRequiredMixin, DetailView):
    model = Programa
    template_name =  "Programa/programa_detail_investigador.html" 
    context_object_name = 'programa'

    def get_queryset(self):
        return Programa.objects.filter(usuario=self.request.user)


def Programa_Delete_Investigador(request,id):
    programa = Programa.objects.get(id=id)
    programa.delete()
    return redirect("Programa_List_Investigador")


def Programa_Update_Investigador(request, programa_id):
    programa = get_object_or_404(Programa, pk=programa_id)
    if request.method == 'POST':
        form = Programa_Form(request.POST, instance=programa)
        if form.is_valid():
            form.save()
        return redirect('Programa_List_Investigador')
    else:
        form = Programa_Form(instance=programa)  
        return render(request, 'Programa/programa_update_investigador.html', {'form': form})
    

#................................Premio..................................

class Premio_Create(LoginRequiredMixin, CreateView):
    model = Premio
    form_class = Premio_Form
    template_name = "Premio/premio_create.html"
    success_url = reverse_lazy('Premio_List_Investigador')
    tipo_premio_form = TipoPremioForm()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  

        if self.request.method == 'POST':
            premiados_ids = self.request.POST.getlist('premiados')
            if premiados_ids:
                # Filtrar solo los que son usuarios y extraer el ID numérico
                usuario_ids = [
                    pid.split('-')[1]
                    for pid in premiados_ids
                    if pid.startswith('usuario-')
                ]
                usuarios_extra = Usuario.objects.filter(id__in=usuario_ids)
                kwargs['extra_usuarios'] = usuarios_extra

        return kwargs


    def form_valid(self, form):
        user = self.request.user
        form.instance.usuario = user
        form.instance.area = user.area
        form.instance.departamento = user.departamento

        # Asegura que tenga un título aunque sea nulo
        if not form.instance.titulo:
            form.instance.titulo = "Premio sin título"

        response = super().form_valid(form)
        premio = self.object

        # Agrega el usuario autenticado como premiado principal
        premiados = form.cleaned_data.get('premiados', [])
        PremioPremiado.objects.create(premio=premio, usuario=user)
        print("Premiados seleccionados en POST:", premiados)

        # Agrega otros premiados si los hay
        for seleccionado in form.cleaned_data.get('premiados', []):
            tipo, id_str = seleccionado.split('-')
            if tipo == 'usuario':
                usuario = Usuario.objects.get(id=int(id_str))
                if usuario.id != user.id:  # Evitar duplicar al usuario autenticado
                    PremioPremiado.objects.get_or_create(premio=premio, usuario=usuario)
            elif tipo == 'colaborador':
                colaborador = Colaborador.objects.get(id=int(id_str))
                PremioPremiado.objects.get_or_create(premio=premio, colaborador=colaborador)


        messages.success(self.request, "Premio creado exitosamente.")
        return response


    def form_invalid(self, form):
        errores = []
        for field, field_errors in form.errors.items():
            if field == '__all__':
                errores.extend(field_errors)
            else:
                field_label = form.fields.get(field).label or field.replace('_', ' ').capitalize()
                for error in field_errors:
                    errores.append(f"{field_label}: {error}")

        mensaje_error = "Hubo un error al crear el Premio. Por favor, corrige los siguientes campos: "
        mensaje_error += " ".join(f"• {e}" for e in errores)

        messages.error(self.request, mensaje_error)

        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seccion_actual'] = 'premios'
        context['tipo_premio_form'] = TipoPremioForm(user=self.request.user)
        context['caracter_premio_form'] = CaracterPremioForm(user=self.request.user)
        context['proyectos'] = Proyecto.objects.filter(aprobacion='Aprobado')
        context['instituciones'] = Institucion.objects.all()
        return context


class Premio_List_Investigador(LoginRequiredMixin, ListView):
    model = Premio
    template_name = "Premio/premio_list_investigador.html" 
    context_object_name = 'premio'

    def get_queryset(self):
        user = self.request.user
        return Premio.objects.filter(premiados_set__usuario=user).distinct().annotate(
            es_creador=Case(
                When(usuario=user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seccion_actual'] = 'premios'

        premios = context['premio']
        
        for p in premios:
            premiados = list(p.premiados())
            if p.usuario in premiados:
                p.contador_participantes = len(premiados)
            else:
                p.contador_participantes = len(premiados)
                
        return context


class Premio_Detail_Investigador(LoginRequiredMixin, DetailView):
    model = Premio
    template_name =  "Premio/premio_detail_investigador.html" 
    context_object_name = 'premio'

    def get_queryset(self):
        user = self.request.user
        return Premio.objects.filter(
            Q(usuario=user) | Q(premiados_set__usuario=user)
        ).distinct()


def Premio_Delete_Investigador(request,id):
    premio = Premio.objects.get(id=id)
    if premio.aprobacion == "aprobado":
        messages.error(request, "No se puede eliminar un premio aprobado.")
        return redirect('Premio_List_Investigador')
    premio.delete()
    return redirect('Premio_List_Investigador')


def Premio_Update_Investigador(request, premio_id):
    premio = get_object_or_404(Premio, pk=premio_id)
    instituciones = Institucion.objects.all()
    proyectos = Proyecto.objects.filter(aprobacion='Aprobado')

    if premio.aprobacion == "aprobado":
        messages.error(request, "No se puede editar un premio aprobado.")
        return redirect('Premio_List_Investigador')

    if request.method == 'POST':
        form = Premio_Form(request.POST, request.FILES, instance=premio, user=request.user)
        if form.is_valid():
            premio = form.save()

            nuevos_premiados = form.cleaned_data.get('premiados', [])

            ids_usuarios = [int(p.split('-')[1]) for p in nuevos_premiados if p.startswith('usuario-')]
            ids_colaboradores = [int(p.split('-')[1]) for p in nuevos_premiados if p.startswith('colaborador-')]

            # Eliminar los que ya no están
            PremioPremiado.objects.filter(premio=premio).exclude(
                Q(usuario__id__in=ids_usuarios) | Q(colaborador__id__in=ids_colaboradores)
            ).delete()

            # Agregar los nuevos
            for seleccionado in nuevos_premiados:
                tipo, id_str = seleccionado.split('-')
                if tipo == 'usuario':
                    usuario = Usuario.objects.get(id=int(id_str))
                    PremioPremiado.objects.get_or_create(premio=premio, usuario=usuario)
                elif tipo == 'colaborador':
                    colaborador = Colaborador.objects.get(id=int(id_str))
                    PremioPremiado.objects.get_or_create(premio=premio, colaborador=colaborador)

            # Asegurar que el usuario principal esté
            if not PremioPremiado.objects.filter(premio=premio, usuario=premio.usuario).exists():
                PremioPremiado.objects.create(premio=premio, usuario=premio.usuario)

            messages.success(request, "Premio actualizado exitosamente.")
            return redirect('Premio_List_Investigador')
    else:
        # Ya no pasamos `initial`, el form lo maneja
        form = Premio_Form(instance=premio, user=request.user)

    return render(request, 'Premio/premio_update_investigador.html', {
        'form': form,
        'instituciones': instituciones,
        'proyectos': proyectos
    })


#................................Perfil..................................
class Perfil_Create_Investigador(LoginRequiredMixin, CreateView):
    model = Perfil
    form_class = Perfil_Form  # Just reference the class, don't instantiate it here
    template_name = "Perfil/perfil_create.html"
    success_url = reverse_lazy('Perfil_Detail_Investigador')
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el Perfil Académico. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Perfil Académico creado exitosamente.")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs   
       

class Perfil_Detail_Investigador(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = "Perfil/perfil_detail.html"
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        # Devuelve todos los perfiles del usuario y toma el primero (no lanza MultipleObjectsReturned)
        return Perfil.objects.filter(usuario=self.request.user).first()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return redirect('Perfil_Create_Investigador')
        context = self.get_context_data(object=self.object)
        # Añadimos proyectos explícitamente al contexto
        context['proyectos'] = self.object.proyecto.all()
        return self.render_to_response(context)
    
    
def Perfil_Update_Investigador(request, perfil_id):
    perfil = get_object_or_404(Perfil, pk=perfil_id)
    
    # Add permission check - ensure the user owns this profile
    if request.user != perfil.usuario:
        raise PermissionDenied("No tienes permiso para editar este perfil.")
    
    if request.method == 'POST':
        form = Perfil_Form(request.POST, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('Perfil_Detail_Investigador')
    else:
        form = Perfil_Form(instance=perfil, user=request.user)
    
    return render(request, 'Perfil/perfil_update_investigador.html', {
        'form': form,
        'perfil': perfil  # Pass the profile object to template if needed
    })


#................................Articulo..................................
def buscar_autores(request):
    query = request.GET.get('q', '')
    usuarios = Usuario.objects.filter(
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query) |
        Q(carnet__icontains=query)
    ).exclude(id=request.user.id)[:10]  # Excluye al usuario actual
    
    resultados = []
    for usuario in usuarios:
        resultados.append({
            'id': usuario.id,
            'nombre_completo': f"{usuario.first_name} {usuario.last_name}",
            'carnet': usuario.carnet
        })
    
    return JsonResponse(resultados, safe=False)
    
    
class Articulo_Publicacion_Create(LoginRequiredMixin, CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = "Articulo/articulo_publicacion_create.html"
    success_url = reverse_lazy('Articulo_Publicacion_Create')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasar el usuario actual al formulario
        kwargs['user'] = self.request.user
        # Pasar los proyectos aprobados al formulario
        kwargs['proyectos'] = Proyecto.objects.filter(aprobacion='Aprobado')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegurarse de que request esté disponible en el contexto
        context['request'] = self.request
        # Agregar los proyectos aprobados al contexto
        context['proyectos'] = Proyecto.objects.filter(aprobacion='Aprobado')
        return context
    
    def form_valid(self, form):
        # Establecer el usuario actual como creador del artículo
        form.instance.usuario = self.request.user
        messages.success(self.request, "Solicitud de Publicación creada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear la Publicación. Por favor, intenta de nuevo.")
        print(form.errors)  # Esto imprimirá los errores en la consola del servidor
        return super().form_invalid(form)
    

class ArticuloCreate(LoginRequiredMixin, CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = "Articulo/articulo_revista_create.html"
    success_url = reverse_lazy('Articulo_List_Investigador')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  

        # Procesar los autores del POST si existen
        if self.request.method == 'POST':
            autores_ids = self.request.POST.getlist('autores')
            if autores_ids:
                usuario_ids = [
                    aid.split('-')[1]
                    for aid in autores_ids
                    if aid.startswith('usuario-')
                ]
                usuarios_extra = Usuario.objects.filter(id__in=usuario_ids)
                kwargs['extra_usuarios'] = usuarios_extra

        return kwargs


    def form_valid(self, form):
        user = self.request.user
        form.instance.usuario = user
        form.instance.area = user.area
        form.instance.departamento = user.departamento

        # Guardar artículo
        response = super().form_valid(form)
        articulo = self.object

        # Agregar el autor principal (usuario autenticado)
        ArticuloAutor.objects.create(articulo=articulo, usuario=user)

        # Agregar otros autores si los hay
        autores = form.cleaned_data.get('autores', [])
        print("Autores seleccionados en POST:", autores)
        for seleccionado in autores:
            tipo, id_str = seleccionado.split('-')
            if tipo == 'usuario':
                usuario = Usuario.objects.get(id=int(id_str))
                if usuario.id != user.id:  # evitar duplicar al creador
                    ArticuloAutor.objects.get_or_create(articulo=articulo, usuario=usuario)
            elif tipo == 'colaborador':
                colaborador = Colaborador.objects.get(id=int(id_str))
                ArticuloAutor.objects.get_or_create(articulo=articulo, colaborador=colaborador)

        messages.success(self.request, "Artículo creado exitosamente.")
        return response


    def form_invalid(self, form):
        errores = []
        for field, field_errors in form.errors.items():
            if field == '__all__':
                errores.extend(field_errors)
            else:
                field_label = form.fields.get(field).label or field.replace('_', ' ').capitalize()
                for error in field_errors:
                    errores.append(f"{field_label}: {error}")

        mensaje_error = "Hubo un error al crear el Artículo. Corrige los siguientes campos: "
        mensaje_error += " ".join(f"• {e}" for e in errores)

        messages.error(self.request, mensaje_error)
        print("Errores de formulario:", form.errors)

        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyectos'] = Proyecto.objects.filter(aprobacion='Aprobado')
        context['PAIS'] = PAIS
        context['IDIOMA'] = IDIOMA
        return context
    

class Articulo_List_Investigador(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "Articulo/articulo_list_investigador.html"
    context_object_name = 'articulo'

    def get_queryset(self):
        # Obtener artículos donde el usuario es creador o colaborador
        user = self.request.user
        queryset = Articulo.objects.filter(
            Q(usuario=user)
        ).distinct().annotate(
            es_creador=Case(
                When(usuario=user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        
        for obj in queryset:
            obj.es_tipo = bool(obj.doi)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seccion_actual'] = 'articulos'
        return context


class Articulo_Detail_Investigador(LoginRequiredMixin, DetailView):
    model = Articulo
    template_name =  "Articulo/articulo_detail_investigador.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articulo = self.get_object()

        Articulo.objects.filter(usuario=self.request.user)
    #Variables para controlar qué formularios mostrar
        context['Articulo_Revista'] = articulo.doi and articulo.issn.strip()!= ''#Variables para controlar qué formularios mostrar
        context['Articulo_Publicacion'] = articulo.volumen and articulo.capitulo.strip()!= ''
        return context


def Articulo_Delete_Investigador(request,id):
    articulo = Articulo.objects.get(id=id)
    if articulo.aprobacion == "aprobado":
        messages.error(request, "No se puede eliminar un artículo aprobado.")
        return redirect('Articulo_List_Investigador')
    articulo.delete()
    return redirect('Articulo_List_Investigador')


def Articulo_Revista_Update_Investigador(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            articulo = form.save()
            messages.success(request, "Artículo de revista actualizado exitosamente.")
            return redirect('Articulo_List_Investigador')
        else:
            messages.error(request, "Error al actualizar el artículo. Verifique los datos.")
    else:
        form = ArticuloForm(instance=articulo)
    
    # Obtener proyectos aprobados para el contexto
    proyectos = Proyecto.objects.filter(aprobacion='Aprobado')
    
    return render(request, 'Articulo/articulo_revista_update_investigador.html', {
        'form': form,
        'articulo': articulo,
        'proyectos': proyectos
    })


def Articulo_Publicacion_Update_Investigador(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            articulo = form.save()
            messages.success(request, "Artículo de publicación actualizado exitosamente.")
            return redirect('Articulo_List_Investigador')
        else:
            messages.error(request, "Error al actualizar el artículo. Verifique los datos.")
    else:
        form = ArticuloForm(instance=articulo)
    
    # Obtener proyectos aprobados para el contexto
    proyectos = Proyecto.objects.filter(aprobacion='Aprobado')
    
    return render(request, 'Articulo/articulo_publicacion_update_investigador.html', {
        'form': form,
        'articulo': articulo,
        'proyectos': proyectos
    })


#.......................Curriculo........................................
class Curriculo_List_Investigador(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        
        # Obtener parámetros de filtro
        filtro_tipo = request.GET.get('tipo', '')
        filtro_rol = request.GET.get('rol', '')
        filtro_estado = request.GET.get('estado', '')
        filtro_anio = request.GET.get('anio', '')
        filtro_departamento = request.GET.get('departamento', '')
        
        # Diccionario para mapear tipos de resultados con sus modelos y campos
        MODEL_CONFIG = {
            'Evento': {
                'model': Evento,
                'nombre_field': 'titulo',
                'filters': Q(usuario=user) | Q(eventos_set__usuario=user)
            },
            'Proyecto': {
                'model': Proyecto,
                'nombre_field': 'nombre_proyecto',
                'filters': Q(usuario=user)
            },
            'Programa': {
                'model': Programa,
                'nombre_field': 'nombre_programa',
                'filters': Q(usuario=user)
            },
            'Premio': {
                'model': Premio,
                'nombre_field': 'titulo',
                'filters': Q(usuario=user)
            },
            'Articulo': {
                'model': Articulo,
                'nombre_field': 'titulo',
                'filters': Q(usuario=user) | Q(articulos_set__usuario=user)
            }
        }
        
        resultados = []
        
        # Aplicar filtro por tipo si está presente
        tipos_a_procesar = [filtro_tipo] if filtro_tipo and filtro_tipo in MODEL_CONFIG else MODEL_CONFIG.keys()
        
        for tipo in tipos_a_procesar:
            config = MODEL_CONFIG[tipo]
            base_filters = config['filters']
            
            # Filtros adicionales
            additional_filters = Q()
            
            # Filtro por rol (creador/colaborador)
            if filtro_rol:
                if filtro_rol == 'Creador':
                    additional_filters &= Q(usuario=user)
                elif filtro_rol == 'Colaborador':
                    # Excluir donde el usuario es creador
                    if tipo in ['Evento', 'Premio', 'Articulo']:
                        additional_filters &= ~Q(usuario=user)
            
            # Filtro por estado
            if filtro_estado:
                additional_filters &= Q(aprobacion=filtro_estado)
            
            # Filtro por año
            if filtro_anio:
                additional_filters &= Q(fecha_create__year=filtro_anio)
            
            # Filtro por departamento
            if filtro_departamento:
                additional_filters &= Q(departamento__nombre_departamento=filtro_departamento)
            
            # Aplicar todos los filtros
            queryset = config['model'].objects.filter(
               base_filters & additional_filters
            ).distinct().order_by('-fecha_create').annotate(
               es_creador=Case(
                    When(usuario=user, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                ),
                tipo_resultado=Value(tipo, output_field=CharField()),
                nombre=F(config['nombre_field']),
                autor_principal=F('usuario'),
                anio=ExtractYear('fecha_create')
            )
            
            resultados.extend(list(queryset))
        
        # Ordenar todos los resultados por fecha (más reciente primero)
        resultados = sorted(resultados, key=lambda x: x.fecha_create, reverse=True)
        
        # Recopilar valores únicos para los filtros
        tipos_unicos = sorted(set(r.tipo_resultado for r in resultados))
        estados_unicos = sorted(set(r.aprobacion for r in resultados if hasattr(r, 'aprobacion') and r.aprobacion))
        anios_unicos = sorted(set(r.fecha_create.year for r in resultados), reverse=True)
        departamentos_unicos = sorted(set(str(r.departamento) for r in resultados if hasattr(r, 'departamento') and r.departamento))
        
        # Agregar contador para enumeración
        for i, resultado in enumerate(resultados, 1):
            resultado.contador = i
        
        return render(request, 'Perfil/curriculo_list_investigador.html', {
            'resultados': resultados,
            'total_resultados': len(resultados),
            'tipos_unicos': tipos_unicos,
            'estados_unicos': estados_unicos,
            'anios_unicos': anios_unicos,
            'departamentos_unicos': departamentos_unicos,
            'filtro_tipo': filtro_tipo,
            'filtro_rol': filtro_rol,
            'filtro_estado': filtro_estado,
            'filtro_anio': filtro_anio,
            'filtro_departamento': filtro_departamento
        })


#........................... exportaciones
class Evento_List(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "General/eventos.html" 
    context_object_name = 'evento'

    def get_queryset(self):
        return Evento.objects.filter(usuario=self.request.user)


class Premio_List(LoginRequiredMixin, ListView):
    model = Premio
    template_name =  "General/premios.html" 
    context_object_name = 'premio'

    def get_queryset(self):
        return Premio.objects.filter(usuario=self.request.user)


class Articulo_List(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "General/articulos.html"
    context_object_name = 'articulo'

    def get_queryset(self):
        queryset = Articulo.objects.filter(usuario=self.request.user)
        for obj in queryset:
            obj.es_tipo = bool(obj.doi)  
        return queryset
    

class Proyecto_List(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name =  "General/proyectos.html" 
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)
