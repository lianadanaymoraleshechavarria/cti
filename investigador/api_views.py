from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from .models import EntidadParticipante, TipoParticipacion, Usuario

@login_required
def api_entidades_search(request):
    """
    API para buscar entidades participantes
    """
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    entidades = EntidadParticipante.objects.filter(
        Q(nombre__icontains=query) | Q(siglas__icontains=query)
    )[:10]
    
    results = []
    for entidad in entidades:
        results.append({
            'id': entidad.id,
            'text': f"{entidad.nombre} ({entidad.siglas})",
            'nombre': entidad.nombre,
            'siglas': entidad.siglas,
            'tipo': entidad.tipo_entidad
        })
    
    return JsonResponse({'results': results})

@login_required
def api_tipos_participacion(request):
    """
    API para obtener tipos de participación
    """
    tipos = TipoParticipacion.objects.all()
    
    results = []
    for tipo in tipos:
        results.append({
            'id': tipo.id,
            'text': tipo.nombre,
            'descripcion': tipo.descripcion
        })
    
    return JsonResponse({'results': results})

@login_required
def api_usuarios_search(request):
    """
    API extendida que mantiene compatibilidad con select2 pero incluye colaboradores
    """
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    results = []
    
    # Buscar usuarios registrados
    usuarios = Usuario.objects.filter(
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query) |
        Q(username__icontains=query)
    ).exclude(is_active=False)[:8]  # Reducir a 8 para dejar espacio a colaboradores
    
    for usuario in usuarios:
        nombre_completo = usuario.get_full_name() or usuario.username
        display_text = f"{nombre_completo} ({usuario.username})"
        
        results.append({
            'id': f"usuario_{usuario.id}",  # Prefijo para distinguir tipo
            'text': display_text,
            'tipo': 'usuario',
            'nombre': nombre_completo,
            'username': usuario.username,
            'email': usuario.email,
            'original_id': usuario.id  # ID original sin prefijo
        })
    
    # Buscar colaboradores externos
    colaboradores = Colaboradores.objects.filter(
        Q(nombre__icontains=query) | 
        Q(apellidos__icontains=query) |
        Q(orci__icontains=query)
    )[:7]  # Máximo 7 colaboradores
    
    for colaborador in colaboradores:
        nombre_completo = f"{colaborador.nombre} {colaborador.apellidos}"
        display_text = nombre_completo
        if colaborador.orci:
            display_text += f" (ORCID: {colaborador.orci})"
        
        results.append({
            'id': f"colaborador_{colaborador.id}",  # Prefijo para distinguir tipo
            'text': display_text,
            'tipo': 'colaborador',
            'nombre': nombre_completo,
            'orci': colaborador.orci or '',
            'original_id': colaborador.id  # ID original sin prefijo
        })
    
    # Ordenar: usuarios primero, luego colaboradores
    results_ordenados = sorted(results, key=lambda x: (0 if x['tipo'] == 'usuario' else 1, x['text']))
    
    return JsonResponse({'results': results_ordenados})


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def crear_entidad_ajax(request):
    """
    API para crear nueva entidad participante via AJAX
    """
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        nombre = data.get('nombre', '').strip()
        siglas = data.get('siglas', '').strip()
        tipo_entidad = data.get('tipo_entidad', '').strip()
        
        if not all([nombre, siglas, tipo_entidad]):
            return JsonResponse({
                'success': False,
                'error': 'Todos los campos son requeridos'
            })
        
        # Verificar si ya existe
        if EntidadParticipante.objects.filter(
            Q(nombre=nombre) | Q(siglas=siglas)
        ).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe una entidad con ese nombre o siglas'
            })
        
        # Crear nueva entidad
        entidad = EntidadParticipante.objects.create(
            nombre=nombre,
            siglas=siglas,
            tipo_entidad=tipo_entidad,
            descripcion=data.get('descripcion', ''),
            creado_por=request.user
        )
        
        return JsonResponse({
            'success': True,
            'entidad': {
                'id': entidad.id,
                'nombre': entidad.nombre,
                'siglas': entidad.siglas,
                'tipo_entidad': entidad.tipo_entidad
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def crear_tipo_participacion_ajax(request):
    """
    API para crear nuevo tipo de participación via AJAX
    """
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        nombre = data.get('nombre', '').strip()
        
        if not nombre:
            return JsonResponse({
                'success': False,
                'error': 'El nombre es requerido'
            })
        
        # Verificar si ya existe
        if TipoParticipacion.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe un tipo de participación con ese nombre'
            })
        
        # Crear nuevo tipo
        tipo = TipoParticipacion.objects.create(
            nombre=nombre,
            descripcion=data.get('descripcion', ''),
            creado_por=request.user
        )
        
        return JsonResponse({
            'success': True,
            'tipo': {
                'id': tipo.id,
                'nombre': tipo.nombre,
                'descripcion': tipo.descripcion
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        })

@login_required
def api_departamentos_por_area(request):
    """
    API para obtener departamentos filtrados por área
    """
    area_id = request.GET.get('area_id')
    if not area_id:
        return JsonResponse({'results': []})
    
    try:
        from .models import Departamento
        departamentos = Departamento.objects.filter(area_id=area_id)
        
        results = []
        for dept in departamentos:
            results.append({
                'id': dept.id,
                'text': dept.nombre,
                'codigo': dept.codigo if hasattr(dept, 'codigo') else ''
            })
        
        return JsonResponse({'results': results})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        })

@login_required
def api_usuarios_por_departamento(request):
    """
    API para obtener usuarios filtrados por departamento
    """
    departamento_id = request.GET.get('departamento_id')
    if not departamento_id:
        return JsonResponse({'results': []})
    
    try:
        usuarios = Usuario.objects.filter(
            departamento_id=departamento_id,
            is_active=True
        )
        
        results = []
        for usuario in usuarios:
            results.append({
                'id': usuario.id,
                'text': f"{usuario.get_full_name()} - {usuario.username}",
                'nombre': usuario.get_full_name(),
                'username': usuario.username,
                'email': usuario.email
            })
        
        return JsonResponse({'results': results})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        })
