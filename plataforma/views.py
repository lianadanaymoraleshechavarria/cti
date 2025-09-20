from .forms import(
                    Perfil_Form_Vicerrector, 
                    Perfil_JefeArea_Form, 
                    Perfil_Jefedepartamento_Form)
from investigador.models import  (Articulo, 
                                  Evento, 
                                  Programa, 
                                  Proyecto, 
                                  Premio,
                                  Perfil, 
                                  Area, 
                                  Departamento,
                                  Categoria_cientifica,
                                  Categoria_docente,
                                  CarcterEvento,
                                  Cargo, Revista_Libro_Conferencia, 
                                  Notificacion, Colaborador,
                                   Indexacion, EventoBase, TipoEvento, TipoPremio, CaracterPremio, Modalidad, EntidadParticipante, TipoPrograma, SectorEstrategico)
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from investigador.forms import (Area_Form, Departamento_Form, CategoriaCientificaForm, CategoriaDocenteForm, CarcterEvento_Form, CaracterPremioForm, 
Cargo_Form, Revista_Libro_Conferencia_Form, 
BasesDatosForm, Colaborador_Form, TipoEventoForm, TipoPremioForm, ModalidadForm, EventoBaseForm)
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_required, pure_admin_required, vicerrector_required, vicedecano_required, jefearea_required, admin_staff_required, jefedepartamento_required
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from .models import PerfilV
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from plataforma.models import Usuario
from plataforma.choices import ROLES_USUARIO
from django.contrib import messages
from django.db.models import Count
from django.conf import settings
from django.http import Http404
from django.db.models import Count, Case, When, IntegerField, Q
from django.views import View
from itertools import chain
import json
from django.db.models.functions import ExtractYear
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import datetime, date
import datetime
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Usuario
from plataforma.choices import ROLES_USUARIO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .choices import obtener_roles_personalizados
from plataforma.models import NombreRol
from plataforma.choices import ROLES_BASE
from dal import autocomplete
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.views.decorators.vary import vary_on_cookie
from plataforma.choices import (
    TIPO_PROYECTO_CHOICES, LINEA_INVESTIGACION_CHOICES, CARACTER_EVENTO, TIPO
)

Usuario = get_user_model()
# API endpoint for dashboard data filtering
@login_required
def api_dashboard_data(request):
    """
    API endpoint to get filtered dashboard data based on year
    """
    year = request.GET.get('year', 'all')
    user = request.user
    
    # Base filters based on user role
    base_filters = {}
    if user.rol == 'Jefe_area' and hasattr(user, 'area') and user.area:
        base_filters['area'] = user.area
    elif user.rol == 'Jefe_departamento' and hasattr(user, 'departamento') and user.departamento:
        base_filters['departamento'] = user.departamento
    
    # Year filtering
    year_filters = {}
    if year != 'all' and year.isdigit():
        year_int = int(year)
        year_filters = {
            'articulos': Q(fecha_creacion__year=year_int),
            'premios': Q(fecha__year=year_int),
            'proyectos': Q(fecha_inicio__year=year_int),
            'eventos': Q(fecha__year=year_int),
            'programas': Q(fecha_create__year=year_int)
        }
    
    # Get filtered data
    def get_filtered_count(model, date_filter_key, **extra_filters):
        queryset = model.objects.filter(**base_filters, **extra_filters)
        if year != 'all' and year.isdigit():
            queryset = queryset.filter(year_filters.get(date_filter_key, Q()))
        return queryset.count()
    
    # Calculate totals
    total_articulos = get_filtered_count(Articulo, 'articulos', aprobacion='Aprobado')
    total_premios = get_filtered_count(Premio, 'premios', aprobacion='Aprobado')
    total_proyectos = get_filtered_count(Proyecto, 'proyectos', aprobacion='Aprobado')
    total_eventos = get_filtered_count(Evento, 'eventos', aprobacion='Aprobado')
    
    # Calculate pending items
    total_articulos_pendientes = get_filtered_count(Articulo, 'articulos', aprobacion='Pendiente')
    total_premios_pendientes = get_filtered_count(Premio, 'premios', aprobacion='Pendiente')
    total_proyectos_pendientes = get_filtered_count(Proyecto, 'proyectos', aprobacion='Pendiente')
    total_eventos_pendientes = get_filtered_count(Evento, 'eventos', aprobacion='Pendiente')
    total_programas_pendientes = get_filtered_count(Programa, 'programas', aprobacion='Pendiente')
    
    # Get chart data based on user role
    if user.rol in ['Vicerrector', 'Administrador']:
        # Investigators by area
        investigadores_query = Perfil.objects.values('area__nombre_area').annotate(count=Count('id'))
        if year != 'all' and year.isdigit():
            # Filter by creation year if available
            investigadores_query = investigadores_query.filter(usuario__date_joined__year=int(year))
        
        data_grafica_investigadores = list(investigadores_query.order_by('area__nombre_area'))
        
        # Awards by area
        premios_query = Premio.objects.filter(aprobacion='Aprobado', **base_filters)
        if year != 'all' and year.isdigit():
            premios_query = premios_query.filter(fecha__year=int(year))
        premios_aprobados_por_area = list(
            premios_query.values('area__nombre_area').annotate(count=Count('id')).order_by('area__nombre_area')
        )
        
    elif user.rol == 'Jefe_area':
        # Data for area head
        area_usuario = user.area
        investigadores_query = Perfil.objects.filter(area=area_usuario).values('departamento__nombre_departamento').annotate(count=Count('id'))
        data_grafica_investigadores = list(investigadores_query.order_by('departamento__nombre_departamento'))
        
        premios_query = Premio.objects.filter(area=area_usuario, aprobacion='Aprobado')
        if year != 'all' and year.isdigit():
            premios_query = premios_query.filter(fecha__year=int(year))
        premios_aprobados_por_area = list(
            premios_query.values('departamento__nombre_departamento').annotate(count=Count('id')).order_by('departamento__nombre_departamento')
        )
        
    elif user.rol == 'Jefe_departamento':
        # Data for department head
        depto_usuario = user.departamento
        investigadores_query = Perfil.objects.filter(departamento=depto_usuario).values('area__nombre_area').annotate(count=Count('id'))
        data_grafica_investigadores = list(investigadores_query.order_by('area__nombre_area'))
        
        premios_query = Premio.objects.filter(departamento=depto_usuario, aprobacion='Aprobado')
        if year != 'all' and year.isdigit():
            premios_query = premios_query.filter(fecha__year=int(year))
        premios_aprobados_por_area = list(
            premios_query.values('area__nombre_area').annotate(count=Count('id')).order_by('area__nombre_area')
        )
    
    # Prepare response data
    response_data = {
        'totals': {
            'articulos': total_articulos,
            'premios': total_premios,
            'proyectos': total_proyectos,
            'eventos': total_eventos
        },
        'pending': {
            'Artículos': total_articulos_pendientes,
            'Premios': total_premios_pendientes,
            'Proyectos': total_proyectos_pendientes,
            'Eventos': total_eventos_pendientes,
            'Programas': total_programas_pendientes
        },
        'charts': {
            'investigadores': data_grafica_investigadores,
            'premios_aprobados': premios_aprobados_por_area
        }
    }
    
    return JsonResponse(response_data)


def get_available_years():
    """
    Get all available years from different models
    """
    years = set()
    
    # Get years from different models
    articulo_years = Articulo.objects.dates('fecha_create', 'year')
    premio_years = Premio.objects.dates('fecha_create', 'year')
    proyecto_years = Proyecto.objects.dates('fecha_inicio', 'year')
    evento_years = Evento.objects.dates('fecha_create', 'year')
    programa_years = Programa.objects.dates('fecha_create', 'year')
    
    # Combine all years
    for date_obj in articulo_years:
        years.add(date_obj.year)
    for date_obj in premio_years:
        years.add(date_obj.year)
    for date_obj in proyecto_years:
        years.add(date_obj.year)
    for date_obj in evento_years:
        years.add(date_obj.year)
    for date_obj in programa_years:
        years.add(date_obj.year)
    
    # Return sorted years (most recent first)
    return sorted(years, reverse=True)


@method_decorator(vary_on_cookie, name='dispatch')
class Dashboard_Vicerrector(LoginRequiredMixin, TemplateView):
    template_name = 'Vicerrector/dashboard_vicerrector.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el año seleccionado
        selected_year = self.request.GET.get('year', 'all')
        
        # Filtros por año
        year_filter = {}
        if selected_year != 'all' and selected_year.isdigit():
            year_int = int(selected_year)
            articulos_filter = Q(fecha_creacion__year=year_int)
            premios_filter = Q(fecha__year=year_int)
            proyectos_filter = Q(fecha_inicio__year=year_int)
            eventos_filter = Q(fecha__year=year_int)
            programas_filter = Q(fecha_create__year=year_int)
        else:
            articulos_filter = Q()
            premios_filter = Q()
            proyectos_filter = Q()
            eventos_filter = Q()
            programas_filter = Q()
        
        # Calcular totales con el filtro por año
        total_articulos = Articulo.objects.filter(articulos_filter).count()
        total_premios = Premio.objects.filter(premios_filter).count()
        total_proyectos = Proyecto.objects.filter(proyectos_filter).count()
        total_eventos = Evento.objects.filter(eventos_filter).count()
        
        # Datos para gráficos
        data_grafica_investigadores = Perfil.objects.values('area__nombre_area').annotate(
            count=Count('id')
        ).order_by('area__nombre_area')
        
        # Elementos pendientes con el filtro por año
        total_articulos_pendientes = Articulo.objects.filter(
            articulos_filter, aprobacion='Pendiente'
        ).count()
        total_premios_pendientes = Premio.objects.filter(
            premios_filter, aprobacion='Pendiente'
        ).count()
        total_proyectos_pendientes = Proyecto.objects.filter(
            proyectos_filter, aprobacion='Pendiente'
        ).count()
        total_eventos_pendientes = Evento.objects.filter(
            eventos_filter, aprobacion='Pendiente'
        ).count()
        total_programas_pendientes = Programa.objects.filter(
            programas_filter, aprobacion='Pendiente'
        ).count()
        
        # Premios aprobados por área con el filtro por año
        premios_aprobados_por_area = Premio.objects.filter(
            premios_filter, aprobacion='Aprobado'
        ).values('area__nombre_area').annotate(
            count=Count('id')
        ).order_by('area__nombre_area')
        
        # Actualizar el contexto
        context.update({
            'investigadores': Perfil.objects.all(),
            'total_articulos': total_articulos,
            'total_premios': total_premios,
            'total_proyectos': total_proyectos,
            'total_eventos': total_eventos,
            'data_grafica_investigadores': list(data_grafica_investigadores),
            'total_articulos_pendientes': total_articulos_pendientes,
            'total_premios_pendientes': total_premios_pendientes,
            'total_proyectos_pendientes': total_proyectos_pendientes,
            'total_eventos_pendientes': total_eventos_pendientes,
            'total_programas_pendientes': total_programas_pendientes,
            'datos_gráfico_pendientes': {
                'Artículos': total_articulos_pendientes,
                'Premios': total_premios_pendientes,
                'Proyectos': total_proyectos_pendientes,
                'Eventos': total_eventos_pendientes,
                'Programas': total_programas_pendientes,
            },
            'premios_aprobados_por_area': list(premios_aprobados_por_area),
            'available_years': get_available_years(),
            'selected_year': selected_year
        })
        
        # Agregar notificaciones si existen
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(
                leida=False
            ).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(
                leida=False
            ).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context

@method_decorator([login_required, pure_admin_required], name='dispatch')
class Dashboard_Admin(LoginRequiredMixin, TemplateView):
    template_name = 'Plataforma/dashboard_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el año seleccionado
        selected_year = self.request.GET.get('year', 'all')
        
        # Filtros por año
        if selected_year != 'all' and selected_year.isdigit():
            year_int = int(selected_year)
            articulos_filter = Q(fecha_creacion__year=year_int)
            premios_filter = Q(fecha__year=year_int)
            proyectos_filter = Q(fecha_inicio__year=year_int)
            eventos_filter = Q(fecha__year=year_int)
            programas_filter = Q(fecha_create__year=year_int)
        else:
            articulos_filter = Q()
            premios_filter = Q()
            proyectos_filter = Q()
            eventos_filter = Q()
            programas_filter = Q()
        
        # Calcular totales con el filtro por año
        total_articulos = Articulo.objects.filter(articulos_filter).count()
        total_premios = Premio.objects.filter(premios_filter).count()
        total_proyectos = Proyecto.objects.filter(proyectos_filter).count()
        total_eventos = Evento.objects.filter(eventos_filter).count()
        
        # Datos para gráficos
        data_grafica_investigadores = Perfil.objects.values('area__nombre_area').annotate(
            count=Count('id')
        ).order_by('area__nombre_area')
        
        # Elementos pendientes con el filtro por año
        total_articulos_pendientes = Articulo.objects.filter(
            articulos_filter, aprobacion='Pendiente'
        ).count()
        total_premios_pendientes = Premio.objects.filter(
            premios_filter, aprobacion='Pendiente'
        ).count()
        total_proyectos_pendientes = Proyecto.objects.filter(
            proyectos_filter, aprobacion='Pendiente'
        ).count()
        total_eventos_pendientes = Evento.objects.filter(
            eventos_filter, aprobacion='Pendiente'
        ).count()
        total_programas_pendientes = Programa.objects.filter(
            programas_filter, aprobacion='Pendiente'
        ).count()
        
        # Premios aprobados por área con el filtro por año
        premios_aprobados_por_area = Premio.objects.filter(
            premios_filter, aprobacion='Aprobado'
        ).values('area__nombre_area').annotate(
            count=Count('id')
        ).order_by('area__nombre_area')
        
        # Actualizar el contexto
        context.update({
            'investigadores': Perfil.objects.all(),
            'investigador_count': Usuario.objects.all(),
            'total_articulos': total_articulos,
            'total_premios': total_premios,
            'total_proyectos': total_proyectos,
            'total_eventos': total_eventos,
            'data_grafica_investigadores': list(data_grafica_investigadores),
            'total_articulos_pendientes': total_articulos_pendientes,
            'total_premios_pendientes': total_premios_pendientes,
            'total_proyectos_pendientes': total_proyectos_pendientes,
            'total_eventos_pendientes': total_eventos_pendientes,
            'total_programas_pendientes': total_programas_pendientes,
            'datos_gráfico_pendientes': {
                'Artículos': total_articulos_pendientes,
                'Premios': total_premios_pendientes,
                'Proyectos': total_proyectos_pendientes,
                'Eventos': total_eventos_pendientes,
                'Programas': total_programas_pendientes,
            },
            'total_usuarios': Usuario.objects.count(),
            'premios_aprobados_por_area': list(premios_aprobados_por_area),
            'available_years': get_available_years(),
            'selected_year': selected_year
        })
        
        # Agregar notificaciones si existen
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(
                leida=False
            ).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(
                leida=False
            ).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context
        

@method_decorator([login_required, jefearea_required], name='dispatch')
class Dashboard_JefeArea(LoginRequiredMixin, TemplateView):
    template_name = 'JefeArea/dashboard_JefeArea.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil_JefeArea = self.request.user
        
        area_JefeArea = perfil_JefeArea.area
        investigadores = Perfil.objects.filter(area=area_JefeArea)

        # Get selected year from request
        selected_year = self.request.GET.get('year', 'all')
        
        # Year filtering
        if selected_year != 'all' and selected_year.isdigit():
            year_int = int(selected_year)
            articulos_filter = Q(fecha_creacion__year=year_int)
            premios_filter = Q(fecha__year=year_int)
            proyectos_filter = Q(fecha_inicio__year=year_int)
            eventos_filter = Q(fecha__year=year_int)
            programas_filter = Q(fecha_create__year=year_int)
        else:
            articulos_filter = Q()
            premios_filter = Q()
            proyectos_filter = Q()
            eventos_filter = Q()
            programas_filter = Q()

        # Calculate totals for the area with year filtering
        total_articulos = Articulo.objects.filter(area=area_JefeArea, aprobacion='Aprobado').filter(articulos_filter).count()
        total_premios = Premio.objects.filter(area=area_JefeArea, aprobacion='Aprobado').filter(premios_filter).count()
        total_proyectos = Proyecto.objects.filter(area=area_JefeArea, aprobacion='Aprobado').filter(proyectos_filter).count()
        total_eventos = Evento.objects.filter(area=area_JefeArea, aprobacion='Aprobado').filter(eventos_filter).count()

        data_grafica_investigadores = Perfil.objects.filter(area=area_JefeArea).values('departamento__nombre_departamento').annotate(count=Count('id')).order_by('departamento__nombre_departamento')

        # Calculate pending items with year filtering
        total_articulos_pendientes = Articulo.objects.filter(area=area_JefeArea, aprobacion='Pendiente').filter(articulos_filter).count()
        total_premios_pendientes = Premio.objects.filter(area=area_JefeArea, aprobacion='Pendiente').filter(premios_filter).count()
        total_proyectos_pendientes = Proyecto.objects.filter(area=area_JefeArea, aprobacion='Pendiente').filter(proyectos_filter).count()
        total_eventos_pendientes = Evento.objects.filter(area=area_JefeArea, aprobacion='Pendiente').filter(eventos_filter).count()
        total_programas_pendientes = Programa.objects.filter(area=area_JefeArea, aprobacion='Pendiente').filter(programas_filter).count()

        # Awards approved by area with year filtering
        premios_aprobados_por_area = Premio.objects.filter(
            area=area_JefeArea, aprobacion='Aprobado'
        ).filter(premios_filter).values('departamento__nombre_departamento').annotate(count=Count('id')).order_by('departamento__nombre_departamento')
        
        eventos_aprobados_por_area = Evento.objects.filter(
            area=area_JefeArea, aprobacion='Aprobado'
        ).filter(eventos_filter).values('departamento__nombre_departamento').annotate(count=Count('id')).order_by('departamento__nombre_departamento')
        
        articulos_aprobados_por_area = Articulo.objects.filter(
            area=area_JefeArea, aprobacion='Aprobado'
        ).filter(articulos_filter).values('departamento__nombre_departamento').annotate(count=Count('id')).order_by('departamento__nombre_departamento')

        # Add data to context
        context.update({
            'investigadores': investigadores,
            'total_articulos': total_articulos,
            'total_premios': total_premios,
            'total_proyectos': total_proyectos,
            'total_eventos': total_eventos,
            'data_grafica_investigadores': list(data_grafica_investigadores),
            'total_articulos_pendientes': total_articulos_pendientes,
            'total_premios_pendientes': total_premios_pendientes,
            'total_proyectos_pendientes': total_proyectos_pendientes,
            'total_eventos_pendientes': total_eventos_pendientes,
            'total_programas_pendientes': total_programas_pendientes,
            'datos_gráfico_pendientes': {
                'Artículos': total_articulos_pendientes,
                'Premios': total_premios_pendientes,
                'Proyectos': total_proyectos_pendientes,
                'Eventos': total_eventos_pendientes,
                'Programas': total_programas_pendientes,
            },
            'premios_aprobados_por_area': list(premios_aprobados_por_area),
            'eventos_aprobados_por_area': list(eventos_aprobados_por_area),
            'articulos_aprobados_por_area': list(articulos_aprobados_por_area),
            'available_years': get_available_years(),
            'selected_year': selected_year
        })
        
        # Add notifications
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context

@method_decorator([login_required, jefedepartamento_required], name='dispatch')
class Dashboard_JefeDepartamento(LoginRequiredMixin, TemplateView):
    template_name = 'JefeDepartamento/dashboard_jefedepartamento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user profile and department
        try:
            perfil_JefeDepartamento = Perfil.objects.get(usuario=self.request.user)
            departamento_JefeDepartamento = perfil_JefeDepartamento.departamento
        except Perfil.DoesNotExist:
            # Fallback to user's department if profile doesn't exist
            departamento_JefeDepartamento = getattr(self.request.user, 'departamento', None)

        if not departamento_JefeDepartamento:
            # Handle case where user has no department assigned
            context.update({
                'error': 'No department assigned to user',
                'available_years': get_available_years(),
                'selected_year': 'all'
            })
            return context

        # Filter investigators by department
        investigadores = Perfil.objects.filter(departamento=departamento_JefeDepartamento)

        # Get selected year from request
        selected_year = self.request.GET.get('year', 'all')
        
        # Year filtering
        if selected_year != 'all' and selected_year.isdigit():
            year_int = int(selected_year)
            articulos_filter = Q(fecha_creacion__year=year_int)
            premios_filter = Q(fecha__year=year_int)
            proyectos_filter = Q(fecha_inicio__year=year_int)
            eventos_filter = Q(fecha__year=year_int)
            programas_filter = Q(fecha_create__year=year_int)
        else:
            articulos_filter = Q()
            premios_filter = Q()
            proyectos_filter = Q()
            eventos_filter = Q()
            programas_filter = Q()

        # Calculate totals for the department with year filtering
        total_articulos = Articulo.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').filter(articulos_filter).count()
        total_premios = Premio.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').filter(premios_filter).count()
        total_proyectos = Proyecto.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').filter(proyectos_filter).count()
        total_eventos = Evento.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').filter(eventos_filter).count()

        # Calculate pending items with year filtering
        total_articulos_pendientes = Articulo.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').filter(articulos_filter).count()
        total_premios_pendientes = Premio.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').filter(premios_filter).count()
        total_proyectos_pendientes = Proyecto.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').filter(proyectos_filter).count()
        total_eventos_pendientes = Evento.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').filter(eventos_filter).count()
        total_programas_pendientes = Programa.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').filter(programas_filter).count()

        # Chart data for investigators by area within the department
        data_grafica_investigadores = Perfil.objects.filter(departamento=departamento_JefeDepartamento).values('area__nombre_area').annotate(count=Count('id')).order_by('area__nombre_area')
        
        # If no data by area, use department as category
        if not data_grafica_investigadores:
            data_grafica_investigadores = [{'departamento': str(departamento_JefeDepartamento), 'count': investigadores.count()}]

        # Awards approved by area within the department with year filtering
        premios_aprobados_por_departamento = Premio.objects.filter(
            departamento=departamento_JefeDepartamento, aprobacion='Aprobado'
        ).filter(premios_filter).values('area__nombre_area').annotate(count=Count('id')).order_by('area__nombre_area')
        
        # If no data by area, use department as category
        if not premios_aprobados_por_departamento:
            total_premios_dept = Premio.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').filter(premios_filter).count()
            premios_aprobados_por_departamento = [{'departamento': str(departamento_JefeDepartamento), 'count': total_premios_dept}]

        # Add data to context
        context.update({
            'investigadores': investigadores,
            'total_articulos': total_articulos,
            'total_premios': total_premios,
            'total_proyectos': total_proyectos,
            'total_eventos': total_eventos,
            'data_grafica_investigadores': list(data_grafica_investigadores),
            'total_articulos_pendientes': total_articulos_pendientes,
            'total_premios_pendientes': total_premios_pendientes,
            'total_proyectos_pendientes': total_proyectos_pendientes,
            'total_eventos_pendientes': total_eventos_pendientes,
            'total_programas_pendientes': total_programas_pendientes,
            'datos_gráfico_pendientes': {
                'Artículos': total_articulos_pendientes,
                'Premios': total_premios_pendientes,
                'Proyectos': total_proyectos_pendientes,
                'Eventos': total_eventos_pendientes,
                'Programas': total_programas_pendientes,
            },
            'premios_aprobados_por_departamento': list(premios_aprobados_por_departamento),
            'available_years': get_available_years(),
            'selected_year': selected_year
        })
        
        # Add notifications
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context


@login_required
def api_eventos_base(request):
    search = request.GET.get('search', '')
    eventos_base = EventoBase.objects.filter(nombre__icontains=search)[:10]
    
    resultados = []
    for evento in eventos_base:
        provincia_nombre = evento.provincia.nombre if evento.provincia else None
        resultados.append({
            'id': evento.id,
            'nombre': evento.nombre,
            'tipo_evento_id': evento.tipo_evento.id,
            'tipo_evento_nombre': evento.tipo_evento.nombre,
            'institucion': evento.institucion_responsable,
            'pais': evento.pais,
            'provincia_id': evento.provincia.id if evento.provincia else None,
            'provincia_nombre': provincia_nombre,
        })
    
    return JsonResponse({'resultados': resultados})


@login_required
def api_crear_evento_base(request):
    if request.method == 'POST':
        form = EventoBaseForm(request.POST)
        if form.is_valid():
            evento_base = form.save()
            provincia_nombre = evento_base.provincia.nombre if evento_base.provincia else None
            return JsonResponse({
                'success': True,
                'evento_base': {
                    'id': evento_base.id,
                    'nombre': evento_base.nombre,
                    'tipo_evento_id': evento_base.tipo_evento.id,
                    'tipo_evento_nombre': evento_base.tipo_evento.nombre,
                    'institucion': evento_base.institucion_responsable,
                    'pais': evento_base.pais,
                    'provincia_id': evento_base.provincia.id if evento_base.provincia else None,
                    'provincia_nombre': provincia_nombre,
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def api_instituciones(request):
    search = request.GET.get('search', '')
    # Obtener instituciones únicas de eventos existentes
    instituciones = set(list(EventoBase.objects.filter(
        institucion_responsable__icontains=search
    ).values_list('institucion_responsable', flat=True).distinct()[:10]))
    
    # Añadir también de los eventos específicos
    instituciones.update(list(Evento.objects.filter(
        institucion_responsable__icontains=search
    ).values_list('institucion_responsable', flat=True).distinct()[:10]))
    
    resultados = []
    for institucion in instituciones:
        resultados.append({
            'nombre': institucion,
        })
    
    return JsonResponse({'resultados': resultados})


@login_required
def api_paises(request):
    search = request.GET.get('search', '')
    # Obtener países únicos de eventos existentes
    paises = set(list(EventoBase.objects.filter(
        pais__icontains=search
    ).values_list('pais', flat=True).distinct()[:10]))
    
    # Añadir también de los eventos específicos
    paises.update(list(Evento.objects.filter(
        pais__icontains=search
    ).values_list('pais', flat=True).distinct()[:10]))
    
    resultados = []
    for pais in paises:
        resultados.append({
            'nombre': pais,
        })
    
    return JsonResponse({'resultados': resultados})


@login_required
def api_provincias(request):
    search = request.GET.get('search', '')
    provincias = Provincia.objects.filter(nombre__icontains=search)[:10]
    
    resultados = []
    for provincia in provincias:
        resultados.append({
            'id': provincia.id,
            'nombre': provincia.nombre,
        })
    
    return JsonResponse({'resultados': resultados})


#Api de revistas 
def api_revistas(request):
    """API para buscar revistas/libros/conferencias"""
    search = request.GET.get('search', '')
    
    # Buscar por título o editorial
    resultados = Revista_Libro_Conferencia.objects.filter(
        Q(titulo__icontains=search) | 
        Q(editorial__icontains=search)
    )[:10]  # Limitar a 10 resultados
    
    data = []
    for item in resultados:
        data.append({
            'id': item.id,
            'titulo': item.titulo,
            'editorial': item.editorial,
            'issn': item.issn or '',
            'isbn': item.isbn or '',
            'pais': item.pais or '',
            'idioma': item.idioma or '',
        })
    
    return JsonResponse(data, safe=False)


@login_required
@permission_required('auth.change_user')
def CambiarRol(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    available_roles = obtener_roles_personalizados()
    
    if request.method == 'POST':
        nuevo_rol = request.POST.get('role')
        
        # Validar que el rol existe
        if nuevo_rol not in dict(ROLES_BASE):
            messages.error(request, 'Rol seleccionado no válido')
            return redirect('CambiarRol', id=usuario.id)
        
        usuario.rol = nuevo_rol
        usuario.save()
        
        messages.success(request, f'Rol actualizado exitosamente a {usuario.get_rol_display()}')
        return redirect('Usuarios')
    
    # Corrección: Solo una plantilla y luego el contexto
    return render(request, "Plataforma/CambiarRol.html", {
        'usuario': usuario,
        'available_roles': available_roles,
        'rol_actual': usuario.get_rol_display(),
    })


class UsuarioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Usuario.objects.all()
        
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q) |
                Q(first_name__icontains=self.q) |
                Q(last_name__icontains=self.q)
            )
        return qs

@login_required
@vicerrector_required
def editar_nombres_roles(request):
    if request.method == "POST":
        clave = request.POST.get("clave")
        nuevo_nombre = request.POST.get("nuevo_nombre").strip()
        
        if not clave or not nuevo_nombre:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('editar_nombres_roles')
        
        # Verificar que la clave existe en ROLES_BASE
        if clave not in dict(ROLES_BASE):
            messages.error(request, "Clave de rol no válida")
            return redirect('editar_nombres_roles')
        
        try:
            # Crear o actualizar el nombre personalizado
            NombreRol.objects.update_or_create(
                codigo=clave,  # Changed from 'clave' to 'codigo' to match your model
                defaults={'nombre_personalizado': nuevo_nombre}
            )
            
            # Limpiar cache
            from django.core.cache import cache
            cache.delete('roles_personalizados_cache')  # Make sure this matches your cache key
            
            messages.success(request, f"Nombre del rol '{clave}' actualizado a '{nuevo_nombre}'")
            return redirect('editar_nombres_roles')
        except Exception as e:
            messages.error(request, f"Error al actualizar el rol: {str(e)}")
            return redirect('editar_nombres_roles')
    
    # Obtener nombres personalizados existentes
    try:
        nombres_personalizados = {
            rol.codigo: rol.nombre_personalizado 
            for rol in NombreRol.objects.all()
        }
    except Exception:
        nombres_personalizados = {}
    
    # Preparar datos para la tabla
    roles_data = []
    for clave, nombre_base in ROLES_BASE:
        roles_data.append({
            'clave': clave,
            'nombre_base': nombre_base,
            'nombre_personalizado': nombres_personalizados.get(clave, nombre_base),
        })
    
    return render(request, "Plataforma/Admin/editar_roles.html", {
        "roles": roles_data,
    })

# Inicio
def Inicio(request):
    return render(request,"plataforma/Inicio.html")

# Usuarios



@login_required
@vicerrector_required  
def Usuarios(request):
    
    areas = Area.objects.all()
    categorias = Categoria_docente.objects.all()
    departamentos = Departamento.objects.select_related('area').order_by('nombre_departamento')
    usuario = Usuario.objects.select_related('area', 'departamento', 'categoria_docente')\
                     .filter(rol__in=['Jefe_area', 'Jefe_departamento', 'Investigador'])
    usuarios =Usuario.objects.all()
    perfil =Perfil.objects.all()
    context = {
        'perfil': perfil,
        'usuarios': usuarios,
        'usuario': usuario,
        'areas': areas,
        'categoria': categorias,
        'departamentos': departamentos
    }
    
    return render(request, "plataforma/Usuarios.html", context)



@login_required
def ListaUsuarios(request):
    usuario = request.user
    
    if usuario.rol == 'Jefe_area':
        usuarios = Usuario.objects.filter(area=usuario.area) if usuario.area else Usuario.objects.none()
    elif usuario.rol in ['Vicerrector', 'Administrador']:
       
        usuarios = Usuario.objects.all()
    else:
   
        usuarios = Usuario.objects.none()

    context = {
        'usuarios': usuarios,
        'rol_usuario': usuario.rol  
    }
    
    return render(request, "Plataforma/lista_usuarios.html", context)

@login_required
@pure_admin_required
def EliminarUsuario(request,id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect("Usuarios")






    

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>ROl JefeArea>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#........................Perfil........................
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Perfil_Create_JefeArea(LoginRequiredMixin, CreateView):
    model = PerfilV
    form_class = Perfil_JefeArea_Form
    template_name = "JefeArea/Perfil/perfil_create_jefearea.html"
    success_url = reverse_lazy('Perfil_Detail_JefeArea')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el Perfil Académico. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Perfil Académico creado exitosamente.")
        return super().form_valid(form)
    
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Perfil_Detail_JefeArea(LoginRequiredMixin, DetailView):
    model = PerfilV
    template_name = "JefeArea/Perfil/perfil_detail_jefearea.html"
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        try:
            return PerfilV.objects.get(usuario=self.request.user)
        except PerfilV.DoesNotExist:
            raise Http404("Perfil no encontrado. Por favor, créalo.")

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('Perfil_Create_JefeArea')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

@jefearea_required 
@login_required
def CambiarRolJefeArea(request, id):
    # Verificar que el usuario actual sea Jefe de área
    if request.user.rol != 'Jefe_area':
        messages.error(request, 'No tiene permisos para realizar esta acción')
        return redirect('home')  # Redirigir a una página principal o adecuada
    
    usuario = get_object_or_404(Usuario, id=id)
    
    # Roles que un Jefe de área puede asignar
    roles_permitidos = [
        ('Jefe_departamento', 'Jefe de departamento'),
        ('Investigador', 'Investigador')
    ]
    
    if request.method == 'POST':
        nuevo_rol = request.POST.get('role')
        
        # Validar que el rol existe y está permitido para este usuario
        roles_permitidos_dict = dict(roles_permitidos)
        if nuevo_rol not in roles_permitidos_dict:
            messages.error(request, 'No tiene permisos para asignar este rol')
            return redirect('CambiarRolJefeArea', id=usuario.id)
        
        usuario.rol = nuevo_rol
        usuario.save()
        
        messages.success(request, f'Rol actualizado exitosamente a {usuario.get_rol_display()}')
        return redirect('List_Investigador_JefeArea_usuario')
    
    return render(request, "JefeArea/cambiar_rol_jefe_area.html", {
        'usuario': usuario,
        'available_roles': roles_permitidos,
        'rol_actual': usuario.get_rol_display(),
    })


@login_required
@jefearea_required   
def Perfil_Update_JefeArea(request, perfil_id):
    perfil = get_object_or_404(PerfilV, pk=perfil_id)
    if request.method == 'POST':
        form = Perfil_JefeArea_Form(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
        return redirect('Perfil_Detail_JefeArea')
    else:
        form = Perfil_JefeArea_Form(instance=perfil)  
        return render(request, 'JefeArea/Perfil/perfil_update_jefearea.html', {'form': form})

#......................................Articulo..............................................................
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Articulo_List_JefeArea(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = 'JefeArea/Articulo/articulo_list_jefearea.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            # Intenta filtrar por área primero
            queryset = Articulo.objects.filter(area=perfil_JefeArea.area)
            if not queryset.exists():  # Si no hay artículos en el área del perfil, muestra todos los artículos
                queryset = Articulo.objects.all()
            return queryset
        except Perfil.DoesNotExist:
            return Articulo.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            context['area'] = perfil_JefeArea.area  # Asumiendo que quieres mostrar el área en el contexto
        except Perfil.DoesNotExist:
            context['area'] = None
        return context

 
    
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Articulo_Detail_JefeArea(LoginRequiredMixin, DetailView):
    model = Articulo
    template_name =  "JefeArea/Articulo/articulo_detail_area.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articulo = self.get_object()

        Articulo.objects.filter(usuario=self.request.user)
    #Variables para controlar qué formularios mostrar
        context['Articulo_Revista'] = articulo.doi and articulo.issn.strip()!= ''#Variables para controlar qué formularios mostrar
        context['Articulo_Publicacion'] = articulo.volumen and articulo.capitulo.strip()!= ''
        return context

@login_required
@jefearea_required
def Articulo_Delete_JefeArea(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    articulo.delete()
    return redirect(reverse_lazy('Articulo_List_JefeArea'))




@admin_staff_required
@login_required
def Cambiar_Estado_Articulo(request, id):
    articulo = get_object_or_404(Articulo, pk=id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['Pendiente', 'No Válido', 'Aprobado']:
            articulo.aprobacion = nuevo_estado
            articulo.save()
            messages.success(request, f'El estado del artículo ha sido cambiado a {nuevo_estado}')
            return redirect('Articulo_List_JefeArea')
    
    estados = ['Pendiente', 'No Válido', 'Aprobado']
    return render(request, "JefeArea/Articulo/cambiar_estado_articulo.html", {
        'estados': estados,
        'articulo': articulo
    })


#...................................Premio...........................................................
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Premio_List_JefeArea(LoginRequiredMixin, ListView):
    model = Premio
    template_name = 'JefeArea/Premio/premio_list_jefearea.html'
    context_object_name = 'premios'

    def get_queryset(self):
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            queryset = Premio.objects.filter(area=perfil_JefeArea.area)
            print(str(queryset.query)) 
            return queryset
        except Perfil.DoesNotExist:
            return Premio.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            context['area'] = perfil_JefeArea.area
        except Perfil.DoesNotExist:
            context['area'] = None  
        return context



@method_decorator([login_required, jefearea_required ], name='dispatch')
class Premio_Detail_JefeArea(LoginRequiredMixin, DetailView):
    model = Premio
    template_name = "JefeArea/Premio/premio_detail_jefearea.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        premio = self.get_object()  
        premios_usuario = Premio.objects.filter(usuario=self.request.user) 
        context['premios_usuario'] = premios_usuario 
        return context

@login_required
@jefearea_required
def Premio_Delete_JefeArea(request, id):
    premio = get_object_or_404(Premio, id=id)
    premio.delete()
    return redirect(reverse_lazy('Premio_List_JefeArea'))

@login_required
@admin_staff_required
def Cambiar_Estado_Premio(request, id):
    premio = get_object_or_404(Premio, pk=id)
    if request.method == 'POST':
        premio.aprobacion = request.POST['estado']
        premio.save()
        messages.success(request, 'El estado del premio ha sido actualizado con éxito.')
        return HttpResponseRedirect(reverse('Premio_List_JefeArea'))
    else:
        estados = [('Pendiente'), ('No Válido'), ('Aprobado')]
        return render(request, "JefeArea/Premio/cambiar_estado_premio.html", {'estados': estados}) 

#........................................Proyecto....................................
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Proyecto_List_JefeArea(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'JefeArea/Proyecto/proyecto_list_jefearea.html'
    context_object_name = 'proyectos'

    def get_queryset(self):
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            queryset = Proyecto.objects.filter(area=perfil_JefeArea.area)  
            return queryset
        except Perfil.DoesNotExist:
            return Proyecto.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            if perfil_JefeArea.area:  
                context['area'] = perfil_JefeArea.area  
            else:
                context['area'] = None  
        except Perfil.DoesNotExist:
            context['area'] = None  
        return context


@method_decorator([login_required, jefearea_required ], name='dispatch')
class Proyecto_Detail_JefeArea(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = "JefeArea/Proyecto/proyecto_detail_jefearea.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()  # Obtiene el premio específico basado en la URL
        proyecto_usuario = Proyecto.objects.filter(usuario=self.request.user)  # Obtiene todos los premios del usuario actual
        context['proyecto_usuario'] = proyecto_usuario  # Agrega los premios del usuario al contexto
        return context

@login_required
@jefearea_required
def Proyecto_Delete_JefeArea(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    proyecto.delete()
    return redirect(reverse_lazy('Proyecto_List_JefeArea'))
    

@login_required
@admin_staff_required
def Cambiar_Estado_Proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=id)
    if request.method == 'POST':
        proyecto.aprobacion = request.POST['estado']
        proyecto.save()
        messages.success(request, 'El estado del proyecto ha sido actualizado con éxito.')
        return HttpResponseRedirect(reverse('Proyecto_List_JefeArea'))
    else:
        estados = [('Pendiente'), ('No Válido'), ('Aprobado')]
        return render(request, "JefeArea/Proyecto/cambiar_estado_proyecto.html", {'estados': estados}) 

#....................Programa..................
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Programa_List_JefeArea(LoginRequiredMixin, ListView):
    model = Programa
    template_name = 'JefeArea/Programa/programa_list_jefearea.html'
    context_object_name = 'programas'

    def get_queryset(self):
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            queryset = Programa.objects.filter(area=perfil_JefeArea.area)  # Asumiendo que 'area' es el campo correcto
            return queryset
        except Perfil.DoesNotExist:
            return Programa.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
          
            if perfil_JefeArea.area:  # Verifica si el usuario tiene un área asociada
                context['area'] = perfil_JefeArea.area  # Usa el área como alternativa
            else:
                context['area'] = None  # No hay área asociada
        except Perfil.DoesNotExist:
            context['area'] = None  # O establece un valor predeterminado según sea necesario
        return context


@method_decorator([login_required, jefearea_required ], name='dispatch')
class Programa_Detail_JefeArea(LoginRequiredMixin, DetailView):
    model = Programa
    template_name = "JefeArea/Programa/programa_detail_jefearea.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programa = self.get_object()  # Obtiene el premio específico basado en la URL
        programa_usuario = Programa.objects.filter(usuario=self.request.user)  # Obtiene todos los premios del usuario actual
        context['programa_usuario'] = programa_usuario  # Agrega los premios del usuario al contexto
        return context

@login_required
@jefearea_required
def Programa_Delete_JefeArea(request, id):
    programa = get_object_or_404(Programa, id=id)
    programa.delete()
    return redirect(reverse_lazy('Programa_List_JefeArea'))

@login_required
@admin_staff_required
def Cambiar_Estado_Programa(request, id):
    programa = get_object_or_404(Programa, pk=id)
    if request.method == 'POST':
        programa.aprobacion = request.POST['estado']
        programa.save()
        messages.success(request, 'El estado del programa ha sido actualizado con éxito.')
        return HttpResponseRedirect(reverse('Programa_List_JefeArea'))
    else:
        estados = [('Pendiente'), ('No Válido'), ('Aprobado')]
        return render(request, "JefeArea/Programa/cambiar_estado_programa.html", {'estados': estados}) 
#....................Evento..................
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Evento_List_JefeArea(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'JefeArea/Evento/evento_list_jefearea.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            queryset = Evento.objects.filter(area=perfil_JefeArea.area)
            return queryset
        except Perfil.DoesNotExist:
            return Evento.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            context['area'] = perfil_JefeArea.area
        except Perfil.DoesNotExist:
            # Maneja el caso en que el usuario no tenga un perfil de JefeArea asociado
            context['area'] = None  # O establece un valor predeterminado según sea necesario
        return context
    

@method_decorator([login_required, jefearea_required ], name='dispatch')
class Evento_Detail_JefeArea(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = "JefeArea/Evento/evento_detail_area.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()  
        evento_usuario = Evento.objects.filter(usuario=self.request.user)  
        context['evento_usuario'] = evento_usuario  
        return context

@login_required
@jefearea_required
def Evento_Delete_JefeArea(request, id):
    evento = get_object_or_404(Evento, id=id)
    evento.delete()
    return redirect(reverse_lazy('Evento_List_JefeArea'))


    
@login_required
@admin_staff_required
def Cambiar_Estado_Evento(request, id):
    evento = get_object_or_404(Evento, pk=id)
    if request.method == 'POST':
        evento.aprobacion = request.POST['estado']
        evento.save()
        messages.success(request, 'El estado del evento ha sido actualizado con éxito.')
        return HttpResponseRedirect(reverse('Evento_List_JefeArea'))
    else:
        estados = [('Pendiente'), ('No Válido'), ('Aprobado')]
        return render(request, "JefeArea/Evento/cambiar_estado_evento.html", {'estados': estados}) 



@method_decorator([login_required, jefearea_required], name='dispatch')
class Informacion_Detail_Investigador_Area(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = "JefeArea/Perfil/informacion_investigador_area.html"
    context_object_name = 'investigador'
    
    def get_object(self, queryset=None):
        # Obtener el usuario por su ID
        usuario_id = self.kwargs.get('pk')
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        # Verificar que el usuario pertenece al área del jefe de área logueado
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            if not perfil_JefeArea.area or usuario.area != perfil_JefeArea.area:
                raise Http404("No tienes permiso para ver este perfil.")
        except Perfil.DoesNotExist:
            raise Http404("No se encontró tu perfil de jefe de área.")
        
        return usuario
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.object
        
        # Intentar obtener el perfil del usuario (Perfil o PerfilV)
        perfil = None
        tipo_perfil = None
        
        try:
            perfil = Perfil.objects.get(usuario=usuario)
            tipo_perfil = 'Perfil'
        except Perfil.DoesNotExist:
            try:
                perfil = Perfil.objects.get(usuario=usuario)
                tipo_perfil = 'Perfil'
            except Perfil.DoesNotExist:
                pass
        
        context['perfil'] = perfil
        context['tipo_perfil'] = tipo_perfil
        
        # Añadir información adicional si es necesario
        if perfil:
            context['tiene_perfil'] = True
        else:
            context['tiene_perfil'] = False
        
        return context






    
#ojojojojooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
@method_decorator([login_required, jefearea_required ], name='dispatch')
class List_Investigador_JefeArea(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'JefeArea/list_investigador_area.html'
    context_object_name = 'investigadores'

    def get_queryset(self):
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            area_JefeArea = perfil_JefeArea.area 
            return Perfil.objects.filter(area=area_JefeArea)
        except ObjectDoesNotExist:
            return redirect('Perfil_Create_JefeArea')


    
#ojojojojooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
@method_decorator([login_required, jefearea_required], name='dispatch')
class List_Investigador_JefeArea_usuario(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'JefeArea/list_investigador_area_usuario.html'
    context_object_name = 'investigadores'  # Cambiado a 'investigadores' para coincidir con la plantilla

    def get_queryset(self):
        """
        Obtiene los usuarios con sus perfiles asociados, filtrados por el área del jefe de área
        """
        try:
            # Intentar obtener el perfil del jefe de área
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            area_JefeArea = perfil_JefeArea.area
            
            if not area_JefeArea:
                messages.error(self.request, "No tienes un área asignada. Contacta al administrador.")
                return []
            
            # Obtener usuarios filtrados por área y excluyendo ciertos roles
            usuarios = Usuario.objects.select_related('area', 'departamento')\
                .filter(area=area_JefeArea)\
                .exclude(rol__in=['Vicerrector', 'admin', 'Jefe_area'])
            
            # Crear una lista de diccionarios con la información combinada de usuario y perfil
            investigadores = []
            
            for usuario in usuarios:
                # Datos básicos del usuario
                investigador = {
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email,
                    'rol': usuario.rol,
                    'area': usuario.area,
                    'departamento': usuario.departamento,
                    'nombre': usuario.first_name,
                    'apellidos': usuario.last_name,
                    'cargo': '',
                    'categoria_docente': '',
                    'categoria_cientifica': '',
                    'tiene_perfil': False
                }
                
                # Intentar obtener el perfil normal
                try:
                    perfil = Perfil.objects.get(usuario=usuario)
                    investigador.update({
                        'nombre': perfil.nombre,
                        'apellidos': perfil.apellidos,
                        'email': perfil.email,
                        'cargo': perfil.cargo,
                        'categoria_docente': perfil.categoria_docente,
                        'categoria_cientifica': perfil.categoria_cientifica,
                        'tiene_perfil': True,
                        'tipo_perfil': 'Perfil'
                    })
                except Perfil.DoesNotExist:
                    # Intentar obtener el perfil V
                    try:
                        perfil = Perfil.objects.get(usuario=usuario)
                        investigador.update({
                            'nombre': perfil.nombre,
                            'apellidos': perfil.apellidos,
                            'email': perfil.email,
                            'cargo': perfil.cargo,
                            'categoria_docente': perfil.categoria_docente,
                            'categoria_cientifica': perfil.categoria_cientifica,
                            'tiene_perfil': True,
                            'tipo_perfil': 'Perfil'
                        })
                    except Perfil.DoesNotExist:
                        pass
                
                investigadores.append(investigador)
            
            return investigadores
            
        except ObjectDoesNotExist:
            messages.error(self.request, "No se encontró tu perfil. Por favor, completa tu perfil primero.")
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Obtener el área del jefe de área logueado
            perfil_JefeArea = Perfil.objects.get(usuario=self.request.user)
            area_JefeArea = perfil_JefeArea.area
            
            if area_JefeArea:
                # Filtrar departamentos por el área del jefe de área
                context['departamentos'] = Departamento.objects.filter(area=area_JefeArea)
                context['area_actual'] = area_JefeArea
                
                # Añadir mensaje si no hay departamentos
                if not context['departamentos'].exists():
                    messages.info(self.request, f"No hay departamentos asociados al área: {area_JefeArea}")
            else:
                context['departamentos'] = Departamento.objects.none()
                context['area_actual'] = None
                messages.warning(self.request, "No tienes un área asignada. Contacta al administrador.")
                
        except ObjectDoesNotExist:
            context['departamentos'] = Departamento.objects.none()
            context['area_actual'] = None
            messages.error(self.request, "No se encontró tu perfil. Por favor, completa tu perfil primero.")
        
        # Añadir opciones de roles para el formulario de cambio de rol
        context['roles'] = [
            ('Investigador', 'Investigador'),
            ('Jefe_departamento', 'Jefe de Departamento')
        ]
        
        return context
        
#....................................................................................................
@method_decorator([login_required, jefearea_required], name='dispatch')
class Curriculo_Investigador_JefeArea(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        # Obtener el usuario por su ID
        usuario = get_object_or_404(Usuario, id=id)
        
        # Verificar que el usuario pertenece al área del jefe de área logueado
        try:
            perfil_JefeArea = Perfil.objects.get(usuario=request.user)
            if not perfil_JefeArea.area or usuario.area != perfil_JefeArea.area:
                messages.error(request, "No tienes permiso para ver este currículum.")
                return redirect('List_Investigador_JefeArea_usuario')
        except Perfil.DoesNotExist:
            messages.error(request, "No se encontró tu perfil de jefe de área.")
            return redirect('List_Investigador_JefeArea_usuario')
        
        # Intentar obtener el perfil del usuario (Perfil o PerfilV)
        perfil = None
        tipo_perfil = None
        
        try:
            perfil = Perfil.objects.get(usuario=usuario)
            tipo_perfil = 'Perfil'
        except Perfil.DoesNotExist:
            try:
                perfil = Perfil.objects.get(usuario=usuario)
                tipo_perfil = 'Perfil'
            except Perfil.DoesNotExist:
                messages.warning(request, "Este usuario no tiene un perfil completo.")
                return render(request, 'JefeArea/curriculo_investigador.html', {
                    'investigador': usuario,
                    'perfil': None,
                    'tipo_perfil': None,
                    'tiene_perfil': False,
                    'resultados': []
                })
        
        # Si llegamos aquí, tenemos un perfil válido
        # Consultas para obtener los resultados académicos del investigador por tipo
        eventos = Evento.objects.filter(usuario=usuario).order_by('fecha_create')
        proyectos = Proyecto.objects.filter(usuario=usuario).order_by('fecha_create')
        programas = Programa.objects.filter(usuario=usuario).order_by('fecha_create')
        premios = Premio.objects.filter(usuario=usuario).order_by('fecha_create')
        articulos = Articulo.objects.filter(usuario=usuario).order_by('fecha_create')
        
        # Combina todas las consultas en una sola lista ordenada por fecha en orden ascendente
        resultados = sorted(chain(eventos, proyectos, programas, premios, articulos), 
                           key=lambda x: x.fecha_create)
        
        # Agregar 'nombre' y 'tipo_resultado' a cada resultado
        for resultado in resultados:
            if isinstance(resultado, Evento):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Evento'
            elif isinstance(resultado, Proyecto):
                resultado.nombre = resultado.nombre_proyecto
                resultado.tipo_resultado = 'Proyecto'
            elif isinstance(resultado, Programa):
                resultado.nombre = resultado.nombre_programa
                resultado.tipo_resultado = 'Programa'
            elif isinstance(resultado, Premio):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Premio'
            elif isinstance(resultado, Articulo):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Articulo'
        
        # Pasa los resultados a la plantilla
        return render(request, 'JefeArea/curriculo_list_user_area.html', {
            'investigador': usuario,
            'perfil': perfil,
            'tipo_perfil': tipo_perfil,
            'tiene_perfil': True,
            'resultados': resultados
        })
#................Inicio JefeArea........... 


#........................... exportaciones  ...........
@method_decorator([login_required, jefearea_required ], name='dispatch')
class Evento_List_Areas(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "JefeArea/General/eventos_area.html" 
    context_object_name = 'evento'

    def get_queryset(self):
        return Evento.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calcular tipos de eventos en general (regional, nacional, internacional)
        tipos_eventos = Evento.objects.values('tipo').annotate(
            count=Count('id')).order_by('tipo')
        context['tipos_eventos_json'] = json.dumps(list(tipos_eventos), cls=DjangoJSONEncoder)

        # Calcular tipos de eventos en general (regional, nacional, internacional)
        caracter_eventos = Evento.objects.values('caracter').annotate(
            count=Count('id')).order_by('tipo')
        context['caracter_eventos_json'] = json.dumps(list(caracter_eventos), cls=DjangoJSONEncoder)
        
        return context

@method_decorator([login_required, jefearea_required ], name='dispatch')
class Premio_List_Areas(LoginRequiredMixin, ListView):
    model = Premio
    template_name = "JefeArea/General/premios_area.html"
    context_object_name = 'premio'

    def get_queryset(self):
        return Premio.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular area con premios pendientes
        area_pendientes = Premio.objects.filter(aprobacion='Pendiente').values('area').annotate(
            count=Count('id'))
        context['area_pendientes_json'] = json.dumps(list(area_pendientes), cls=DjangoJSONEncoder)
        
        # Calcular tipos de premios por area
        tipos_premios_por_area = Premio.objects.values('area', 'tipo').annotate(
            count=Count('id')).order_by('area', 'tipo')
        context['tipos_premios_por_area_json'] = json.dumps(list(tipos_premios_por_area), cls=DjangoJSONEncoder)
        
        # Calcular tipos de premios en general (regional, nacional, internacional)
        tipos_premios = Premio.objects.values('tipo').annotate(
            count=Count('id')).order_by('tipo')
        context['tipos_premios_json'] = json.dumps(list(tipos_premios), cls=DjangoJSONEncoder)
        
        return context


@method_decorator([login_required, jefearea_required], name='dispatch')
class Articulo_List_Areas(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "JefeArea/General/articulos_area.html"
    context_object_name = 'articulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Conteo de revistas y publicaciones
        revistas = Articulo.objects.exclude(doi__exact='').exclude(doi__isnull=True).count()
        publicaciones = Articulo.objects.filter(Q(doi__exact='') | Q(doi__isnull=True)).count()

        # Agregar los conteos al contexto
        context['revistas'] = revistas
        context['publicaciones'] = publicaciones

        # Obtener todas las áreas desde la base de datos
        areas = Area.objects.all()
        conteos_por_area = []

        for area in areas:
            total_articulos = Articulo.objects.filter(area=area).count()
            revistas_area = Articulo.objects.filter(area=area).exclude(doi__exact='').exclude(doi__isnull=True).count()
            publicaciones_area = total_articulos - revistas_area

            conteos_por_area.append({
                'area': area.nombre_area,  # Usamos el campo 'nombre' del área
                'total': total_articulos,
                'revistas': revistas_area,
                'publicaciones': publicaciones_area
            })

        context['conteos_por_area'] = conteos_por_area

        return context


@method_decorator([login_required, jefearea_required ], name='dispatch')   
class Proyecto_List_Areas(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "JefeArea/General/proyectos_area.html"
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular la cantidad de proyectos por estado
        estados_proyectos = Proyecto.objects.values('estado_proyecto').annotate(count=Count('id')).order_by('estado_proyecto')
        context['estados_proyectos_json'] = json.dumps(list(estados_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por departamento
        departamentos_proyectos = Proyecto.objects.values('departamento').annotate(count=Count('id')).order_by('departamento')
        context['departamentos_proyectos_json'] = json.dumps(list(departamentos_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por subtipo de proyecto
        subtipos_proyectos = Proyecto.objects.values('subtipo_proyecto').annotate(count=Count('id')).order_by('subtipo_proyecto')
        context['subtipos_proyectos_json'] = json.dumps(list(subtipos_proyectos), cls=DjangoJSONEncoder)
        
        sector_estrategico = Proyecto.objects.values('sector_estrategico').annotate(count=Count('id')).order_by('sector_estrategico')
        context['sector_estrategico'] = json.dumps(list(sector_estrategico), cls=DjangoJSONEncoder)
        
        return context

#ListaPograma        
@method_decorator([login_required, jefearea_required ], name='dispatch')   
class Programa_List_Areas(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "JefeArea/General/programas_area.html"
    context_object_name = 'programa'

    def get_queryset(self):
        return Programa.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
         # Calcular la cantidad de proyectos por departamento

        
        sector_estrategico = Programa.objects.values('sector_estrategico').annotate(count=Count('id')).order_by('sector_estrategico')
        context['sector_estrategico'] = json.dumps(list(sector_estrategico), cls=DjangoJSONEncoder)
        
        return context
    
#..........................................................................................


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>ROl jefedepartamento>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#........................Perfil........................
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Perfil_Create_JefeDepartamento(LoginRequiredMixin, CreateView):
    model = PerfilV
    form_class = Perfil_Jefedepartamento_Form
    template_name = "JefeDepartamento/Perfil/perfil_create_jefedepartamento.html"
    success_url = reverse_lazy('Perfil_Detail_JefeDepartamento')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el Perfil Académico. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Perfil Académico creado exitosamente.")
        return super().form_valid(form)
    
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Perfil_Detail_JefeDepartamento(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = "JefeDepartamento/Perfil/perfil_detail_JefeDepartamento.html"
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        try:
            return Perfil.objects.get(usuario=self.request.user)
        except Perfil.DoesNotExist:
            raise Http404("Perfil no encontrado. Por favor, créalo.")

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('Perfil_Create_JefeDepartamento')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

@login_required
@jefedepartamento_required   
def Perfil_Update_JefeDepartamento(request, perfil_id):
    perfil = get_object_or_404(PerfilV, pk=perfil_id)
    if request.method == 'POST':
        form = Perfil_Jefedepartamento_Form(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
        return redirect('Perfil_Detail_JefeDepartamento')
    else:
        form = Perfil_Jefedepartamento_Form(instance=perfil)  
        return render(request, 'JefeDepartamento/Perfil/perfil_update_Jefedepartamento.html', {'form': form})

#......................................Articulo..............................................................
@method_decorator([login_required, jefedepartamento_required], name='dispatch')
class Articulo_List_JefeDepartamento(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = 'JefeDepartamento/Articulo/articulo_list_jefedepartamento.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        try:
            perfil_Jefedepartamento = Perfil.objects.get(usuario=self.request.user)
            # Filtrar solo por departamento del jefe, sin fallback a todos
            return Articulo.objects.filter(departamento=perfil_Jefedepartamento.departamento)
        except Perfil.DoesNotExist:
            return Articulo.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_Jefedepartamento = Perfil.objects.get(usuario=self.request.user)
            context['departamento'] = perfil_Jefedepartamento.departamento  # Corregido: usar departamento en lugar de área
        except Perfil.DoesNotExist:
            context['departamento'] = None
        return context

 
    
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Articulo_Detail_JefeDepartamento(LoginRequiredMixin, DetailView):
    model = Articulo
    template_name =  "JefeDepartamento/Articulo/articulo_detail_departamento.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articulo = self.get_object()

        Articulo.objects.filter(usuario=self.request.user)
    #Variables para controlar qué formularios mostrar
        context['Articulo_Revista'] = articulo.doi and articulo.issn.strip()!= ''#Variables para controlar qué formularios mostrar
        context['Articulo_Publicacion'] = articulo.volumen and articulo.capitulo.strip()!= ''
        return context

@login_required
@jefedepartamento_required
def Articulo_Delete_JefeDepartamento(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    articulo.delete()
    return redirect(reverse_lazy('Articulo_List_Jefedepartamento'))

#...................................Premio...........................................................
@method_decorator([login_required, jefedepartamento_required], name='dispatch')
class Premio_List_JefeDepartamento(LoginRequiredMixin, ListView):
    model = Premio
    template_name = 'JefeDepartamento/Premio/premio_list.html'
    context_object_name = 'premios'

    def get_queryset(self):
        """
        Obtiene solo los premios del departamento del jefe
        """
        try:
            perfil = Perfil.objects.select_related('departamento').get(usuario=self.request.user)
            
            if not hasattr(perfil, 'departamento') or not perfil.departamento:
                return Premio.objects.none()
                
            return Premio.objects.filter(departamento=perfil.departamento)
            
        except Perfil.DoesNotExist:
            return Premio.objects.none()

    def get_context_data(self, **kwargs):
        """
        Agrega información del departamento al contexto
        """
        context = super().get_context_data(**kwargs)
        
        try:
            perfil = Perfil.objects.select_related('departamento').get(usuario=self.request.user)
            context['departamento'] = perfil.departamento
            context['jefe_departamento'] = perfil  # Agrega todo el perfil por si necesitas más datos
        except Perfil.DoesNotExist:
            context['departamento'] = None
            context['jefe_departamento'] = None
            
        return context

@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Premio_Detail_JefeDepartamento(LoginRequiredMixin, DetailView):
    model = Premio
    template_name = "JefeDepartamento/Premio/premio_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        premio = self.get_object()  
        premios_usuario = Premio.objects.filter(usuario=self.request.user) 
        context['premios_usuario'] = premios_usuario 
        return context

@login_required
@jefedepartamento_required
def Premio_Delete_JefeDepartamento(request, id):
    premio = get_object_or_404(Premio, id=id)
    premio.delete()
    return redirect(reverse_lazy('Premio_List_JefeDepartamento'))

#........................................Proyecto....................................
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Proyecto_List_JefeDepartamento(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'JefeDepartamento/Proyecto/proyecto_list.html'
    context_object_name = 'proyectos'

def get_queryset(self):
    try:
        perfil = Perfil.objects.get(usuario=self.request.user)
        # Aquí el problema puede ser que filtras por 'area' en lugar de 'departamento'
        if not perfil.area:
            return Proyecto.objects.none()
            
        return Proyecto.objects.filter(area=perfil.area)
    except Perfil.DoesNotExist:
        return Proyecto.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_Jefedepartamento = Perfil.objects.get(usuario=self.request.user)
            if perfil_Jefedepartamento.area:  
                context['departamento'] = perfil_Jefedepartamento.area  
            else:
                context['departamento'] = None  
        except Perfil.DoesNotExist:
            context['departamento'] = None  
        return context


@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Proyecto_Detail_JefeDepartamento(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = "JefeDepartamento/Proyecto/proyecto_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()  # Obtiene el premio específico basado en la URL
        proyecto_usuario = Proyecto.objects.filter(usuario=self.request.user)  # Obtiene todos los premios del usuario actual
        context['proyecto_usuario'] = proyecto_usuario  # Agrega los premios del usuario al contexto
        return context

@login_required
@jefedepartamento_required
def Proyecto_Delete_JefeDepartamento(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    proyecto.delete()
    return redirect(reverse_lazy('Proyecto_List_Jefedepartamento'))
    

#....................Programa..................
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Programa_List_JefeDepartamento(LoginRequiredMixin, ListView):
    model = Programa
    template_name = 'JefeDepartamento/Programa/programa_list.html'
    context_object_name = 'programas'

    def get_queryset(self):
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if not perfil.departamento:
                return Programa.objects.none()
                
            return Programa.objects.filter(departamento=perfil.departamento)
        except Perfil.DoesNotExist:
            return Programa.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_Jefedepartamento = Perfil.objects.get(usuario=self.request.user)
            # Asumiendo que quieres mostrar la departamento o área en el contexto para su uso en la plantilla
            if perfil_Jefedepartamento.departamento:  # Verifica si el usuario tiene un área asociada
                context['departamento'] = perfil_Jefedepartamento.departamento  # Usa el área como alternativa
            else:
                context['departamento'] = None  # No hay área asociada
        except Perfil.DoesNotExist:
            context['departamento'] = None  # O establece un valor predeterminado según sea necesario
        return context


@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Programa_Detail_JefeDepartamento(LoginRequiredMixin, DetailView):
    model = Programa
    template_name = "Jefedepartamento/Programa/programa_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programa = self.get_object()  # Obtiene el premio específico basado en la URL
        programa_usuario = Programa.objects.filter(usuario=self.request.user)  # Obtiene todos los premios del usuario actual
        context['programa_usuario'] = programa_usuario  # Agrega los premios del usuario al contexto
        return context

@login_required
@jefedepartamento_required
def Programa_Delete_JefeDepartamento(request, id):
    programa = get_object_or_404(Programa, id=id)
    programa.delete()
    return redirect(reverse_lazy('Programa_List_Jefedepartamento'))


#....................Evento..................
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Evento_List_JefeDepartamento(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'Jefedepartamento/Evento/evento_list_departamento.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if not perfil.departamento:
                return Evento.objects.none()
                
            return Evento.objects.filter(departamento=perfil.departamento)
        except Perfil.DoesNotExist:
            return Evento.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            perfil_Jefedepartamento = Perfil.objects.get(usuario=self.request.user)
            context['departamento'] = perfil_Jefedepartamento.departamento
        except Perfil.DoesNotExist:
            # Maneja el caso en que el usuario no tenga un perfil de Jefedepartamento asociado
            context['departamento'] = None  # O establece un valor predeterminado según sea necesario
        return context
    

@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Evento_Detail_JefeDepartamento(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = "JefeDepartamento/Evento/evento_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()  
        evento_usuario = Evento.objects.filter(usuario=self.request.user)  
        context['evento_usuario'] = evento_usuario  
        return context

@login_required
@jefedepartamento_required
def Evento_Delete_JefeDepartamento(request, id):
    evento = get_object_or_404(Evento, id=id)
    evento.delete()
    return redirect(reverse_lazy('Evento_List_Jefedepartamento'))

@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Informacion_Detail_Investigador_Departamento(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = "JefeDepartamento/Perfil/informacion_investigador.html"

#ojojojojooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class List_Investigador_JefeDepartamento(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'JefeDepartamento/list_investigador.html'
    context_object_name = 'investigadores'

def get_queryset(self):
        try:
            perfil_Jefedepartamento = Perfil.objects.get(usuario=self.request.user)
            departamento_Jefedepartamento = perfil_Jefedepartamento.departamento  
            return Perfil.objects.filter(departamento=departamento_Jefedepartamento)
        except ObjectDoesNotExist:
     
            return redirect('Perfil_Create_JefeDepartamento')
            
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Area.objects.all()
        context['departamentos'] = Departamento.objects.select_related('area').order_by('nombre_departamento')
        return context
        

#....................................................................................................
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Curriculo_Investigador_Departamento(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        # Obtén el perfil del investigador basado en el ID proporcionado en la URL
        perfil_investigador = get_object_or_404(Perfil, pk=id)
        
        # Consultas para obtener los resultados académicos del investigador por tipo
        eventos = Evento.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        proyectos = Proyecto.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        programas = Programa.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        premios = Premio.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        articulos = Articulo.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        
        # Combina todas las consultas en una sola lista ordenada por fecha en orden ascendente
        resultados = sorted(chain(eventos, proyectos, programas, premios, articulos), key=lambda x: x.fecha_create)
        
        # Agregar 'nombre' y 'tipo_resultado' a cada resultado
        for resultado in resultados:
            if isinstance(resultado, Evento):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Evento'
            elif isinstance(resultado, Proyecto):
                resultado.nombre = resultado.nombre_proyecto
                resultado.tipo_resultado = 'Proyecto'
            elif isinstance(resultado, Programa):
                resultado.nombre = resultado.nombre_programa
                resultado.tipo_resultado = 'Programa'
            elif isinstance(resultado, Premio):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Premio'
            elif isinstance(resultado, Articulo):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Articulo'
        
        # Pasa los resultados a la plantilla
        return render(request, 'JefeDepartamento/curriculo_list_user.html', {'resultados': resultados, 'perfil_investigador': perfil_investigador})
    


#........................... exportaciones  ...........
@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Evento_List_Departamento(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "JefeDepartamento/Evento/evento_list_departamento.html" 
    context_object_name = 'evento'

    def get_queryset(self):
        return Evento.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calcular tipos de eventos en general (regional, nacional, internacional)
        tipos_eventos = Evento.objects.values('tipo').annotate(
            count=Count('id')).order_by('tipo')
        context['tipos_eventos_json'] = json.dumps(list(tipos_eventos), cls=DjangoJSONEncoder)

        # Calcular tipos de eventos en general (regional, nacional, internacional)
        caracter_eventos = Evento.objects.values('caracter').annotate(
            count=Count('id')).order_by('tipo')
        context['caracter_eventos_json'] = json.dumps(list(caracter_eventos), cls=DjangoJSONEncoder)
        
        return context

@method_decorator([login_required, jefedepartamento_required ], name='dispatch')
class Premio_List_Departamento(LoginRequiredMixin, ListView):
    model = Premio
    template_name = "JefeDepartamento/General/premios_departamento.html"
    context_object_name = 'premio'

    def get_queryset(self):
        return Premio.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular departamentos con premios pendientes
        departamentos_pendientes = Premio.objects.filter(aprobacion='Pendiente').values('departamento').annotate(
            count=Count('id'))
        context['departamentos_pendientes_json'] = json.dumps(list(departamentos_pendientes), cls=DjangoJSONEncoder)
        
        # Calcular tipos de premios por departamento
        tipos_premios_por_departamento = Premio.objects.values('departamento', 'tipo').annotate(
            count=Count('id')).order_by('departamento', 'tipo')
        context['tipos_premios_por_departamento_json'] = json.dumps(list(tipos_premios_por_departamento), cls=DjangoJSONEncoder)
        
        # Calcular tipos de premios en general (regional, nacional, internacional)
        tipos_premios = Premio.objects.values('tipo').annotate(
            count=Count('id')).order_by('tipo')
        context['tipos_premios_json'] = json.dumps(list(tipos_premios), cls=DjangoJSONEncoder)
        
        return context

@method_decorator([login_required, jefedepartamento_required], name='dispatch')
class Articulo_List_Departamento(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "JefeDepartamento/General/articulos_departamento.html"
    context_object_name = 'articulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Conteo de revistas y publicaciones
        revistas = Articulo.objects.exclude(doi__exact='').exclude(doi__isnull=True).count()
        publicaciones = Articulo.objects.filter(Q(doi__exact='') | Q(doi__isnull=True)).count()

        # Agregar los conteos al contexto
        context['revistas'] = revistas
        context['publicaciones'] = publicaciones

        # Obtener todas las areas desde la base de datos
        areas = Area.objects.all()
        conteos_por_area = []

        # Obtener todas los departamentos desde la base de datos
        departamentos = Departamento.objects.all()
        conteos_por_departamento = []

        for departamento in departamentos:
            total_articulos = Articulo.objects.filter(departamento=departamento).count()
            revistas_departamento = Articulo.objects.filter(departamento=departamento).exclude(doi__exact='').exclude(doi__isnull=True).count()
            publicaciones_departamento = total_articulos - revistas_departamento

            conteos_por_departamento.append({
                'departamento': departamento.nombre_departamento,  
                'total': total_articulos,
                'revistas': revistas_departamento,
                'publicaciones': publicaciones_departamento
            })

        context['conteos_por_departamento'] = conteos_por_departamento

        return context

@method_decorator([login_required, jefedepartamento_required ], name='dispatch')   
class Proyecto_List_Departamento(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "JefeDepartamento/General/proyectos_departamento.html"
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular la cantidad de proyectos por estado
        estados_proyectos = Proyecto.objects.values('estado_proyecto').annotate(count=Count('id')).order_by('estado_proyecto')
        context['estados_proyectos_json'] = json.dumps(list(estados_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por departamento
        departamentos_proyectos = Proyecto.objects.values('departamento').annotate(count=Count('id')).order_by('departamento')
        context['departamentos_proyectos_json'] = json.dumps(list(departamentos_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por subtipo de proyecto
        subtipos_proyectos = Proyecto.objects.values('subtipo_proyecto').annotate(count=Count('id')).order_by('subtipo_proyecto')
        context['subtipos_proyectos_json'] = json.dumps(list(subtipos_proyectos), cls=DjangoJSONEncoder)
        
        sector_estrategico = Proyecto.objects.values('sector_estrategico').annotate(count=Count('id')).order_by('sector_estrategico')
        context['sector_estrategico'] = json.dumps(list(sector_estrategico), cls=DjangoJSONEncoder)
        
        return context
    
#..........................................................................................




#>>>>>>>>>>>>>>>>>>>>>>>>>    VICERRECTOR       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@method_decorator([login_required, admin_staff_required], name='dispatch')
class ReporteCompletoView(LoginRequiredMixin, TemplateView):
    template_name = 'reporte.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener datos para filtros
        context['areas'] = Area.objects.all().order_by('nombre_area')
        
        # Obtener departamentos con su área relacionada para el filtrado
        context['departamentos'] = Departamento.objects.select_related('area').order_by('nombre_departamento')
        
        # Obtener caracteres de evento desde el modelo CarcterEvento
        context['categorias_evento'] = CarcterEvento.objects.all().order_by('nombre_caracter_evento')
        
        # Obtener caracteres de evento desde el modelo Tio
        context['tipos_evento'] = TipoEvento.objects.all().order_by('nombre')  
                
        # Usar las tuplas de choices directamente
        context['tipos_proyecto'] = TIPO_PROYECTO_CHOICES
        context['lineas_investigacion'] = LINEA_INVESTIGACION_CHOICES
        context['tipos_premio'] = CARACTER_EVENTO
        
        # Obtener años para filtros de manera correcta
        context['anios_premios'] = Premio.objects.filter(aprobacion='Aprobado').dates('fecha_create', 'year')
        context['anios_articulos'] = Articulo.objects.filter(aprobacion='Aprobado').dates('fecha_creacion', 'year')
        
        # Filtrar datos según el rol del usuario
        if self.request.user.rol in ['Administrador', 'Vicerrector']:
            # Usar select_related para optimizar consultas con ForeignKey
            context['eventos'] = Evento.objects.filter(aprobacion='Aprobado').select_related(
                'modalidad', 'area', 'departamento', 'usuario', 'tipo'
            ).order_by('-fecha_create')
            
            context['proyectos'] = Proyecto.objects.filter(aprobacion='Aprobado').select_related(
                'area', 'departamento', 'usuario'
            ).order_by('-fecha_inicio')
            
            context['programas'] = Programa.objects.filter(aprobacion='Aprobado').select_related( 'usuario'
            ).order_by('nombre_programa')
            
            context['premios'] = Premio.objects.filter(aprobacion='Aprobado').select_related(
                'area', 'departamento', 'usuario'
            ).order_by('-fecha_create')
            
            context['articulos'] = Articulo.objects.filter(aprobacion='Aprobado').select_related(
                'area', 'departamento', 'usuario'
            ).prefetch_related('autores').order_by('-fecha_creacion')
        
        # Para jefe de área - solo su área
        elif self.request.user.rol == 'Jefe_area' and hasattr(self.request.user, 'area'):
            area_usuario = self.request.user.area
            
            context['eventos'] = Evento.objects.filter(
                area=area_usuario, aprobacion='Aprobado'
            ).select_related('modalidad', 'area', 'departamento', 'usuario').order_by('-fecha_create')
            
            context['proyectos'] = Proyecto.objects.filter(
                area=area_usuario, aprobacion='Aprobado'
            ).select_related('area', 'departamento', 'usuario').order_by('-fecha_inicio')
            
            context['programas'] = Programa.objects.filter(
                area=area_usuario, aprobacion='Aprobado'
            ).select_related( 'usuario').order_by('nombre_programa')
            
            context['premios'] = Premio.objects.filter(
                area=area_usuario, aprobacion='Aprobado'
            ).select_related('area', 'departamento', 'usuario').prefetch_related('premiados').order_by('-fecha')
            
            context['articulos'] = Articulo.objects.filter(
                area=area_usuario, aprobacion='Aprobado'
            ).select_related('area', 'departamento', 'usuario').prefetch_related('autores').order_by('-fecha_creacion')
            
            # Filtrar departamentos solo de esta área
            context['departamentos'] = context['departamentos'].filter(area=area_usuario)
        
        # Para jefe de departamento - solo su departamento
        elif self.request.user.rol == 'Jefe_departamento' and hasattr(self.request.user, 'departamento'):
            depto_usuario = self.request.user.departamento
            
            context['eventos'] = Evento.objects.filter(
                departamento=depto_usuario, aprobacion='Aprobado'
            ).select_related('modalidad', 'area', 'departamento', 'usuario').order_by('-fecha_create')
            
            context['proyectos'] = Proyecto.objects.filter(
                departamento=depto_usuario, aprobacion='Aprobado'
            ).select_related('area', 'departamento', 'usuario').order_by('-fecha_inicio')
            
            context['programas'] = Programa.objects.filter(
                departamento=depto_usuario, aprobacion='Aprobado'
            ).select_related( 'usuario').order_by('nombre_programa')
            
            context['premios'] = Premio.objects.filter(
                departamento=depto_usuario, aprobacion='Aprobado'
            ).select_related('area', 'departamento', 'usuario').prefetch_related('premiados').order_by('-fecha_create')
            
            context['articulos'] = Articulo.objects.filter(
                departamento=depto_usuario, aprobacion='Aprobado'
            ).select_related('area', 'departamento', 'usuario').prefetch_related('autores').order_by('-fecha_creacion')
            
            # Filtrar áreas y departamentos
            context['areas'] = Area.objects.filter(id=depto_usuario.area.id)
            context['departamentos'] = context['departamentos'].filter(id=depto_usuario.id)
        
        return context
#................................Perfil..................................
@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Perfil_Create_Vicerrector(LoginRequiredMixin, CreateView):
    model = PerfilV
    form_class = Perfil_Form_Vicerrector
    template_name = "Vicerrector/Perfil/perfil_create_vicerrector.html"
    success_url = reverse_lazy('Perfil_Detail_Vicerrector')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el Perfil. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Perfil creado exitosamente.")
        return super().form_valid(form)
    

@method_decorator([login_required, vicerrector_required], name='dispatch')
class Perfil_Detail_Vicerrector(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = "Vicerrector/Perfil/perfil_detail_vicerrector.html"
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        try:
            return Perfil.objects.get(usuario=self.request.user)
        except Perfil.DoesNotExist:
            raise Http404("Perfil no encontrado. Por favor, créalo.")

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('Perfil_Create_Vicerrector')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

@vicerrector_required 
@login_required
def CambiarRolVicerrector(request, id):
    # Verificar que el usuario actual sea Vicerrector
    if request.user.rol != 'Vicerrector':
        messages.error(request, 'No tiene permisos para realizar esta acción')
        return redirect('home')  # Redirigir a una página principal o adecuada
    
    usuario = get_object_or_404(Usuario, id=id)
    
    # Roles que un Vicerrector puede asignar
    roles_permitidos = [
        ('Jefe_area', 'Jefe de area'),
        ('Jefe_departamento', 'Jefe de departamento'),
        ('Investigador', 'Investigador')
    ]
    
    if request.method == 'POST':
        nuevo_rol = request.POST.get('role')
        
        # Validar que el rol existe y está permitido para este usuario
        roles_permitidos_dict = dict(roles_permitidos)
        if nuevo_rol not in roles_permitidos_dict:
            messages.error(request, 'No tiene permisos para asignar este rol')
            return redirect('CambiarRolVicerrector', id=usuario.id)
        
        usuario.rol = nuevo_rol
        usuario.save()
        
        messages.success(request, f'Rol actualizado exitosamente a {usuario.get_rol_display()}')
        return redirect('List_Investigador_Vicerrector_Usuario')
    
    return render(request, "Vicerrector/cambiar_rol_vicerrector.html", {
        'usuario': usuario,
        'available_roles': roles_permitidos,
        'rol_actual': usuario.get_rol_display(),
    })
    

@login_required
@vicerrector_required 
def Perfil_Update_Vicerrector(request, perfil_id):
    perfil = get_object_or_404(PerfilV, pk=perfil_id)
    if request.method == 'POST':
        form = Perfil_Form_Vicerrector(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
        return redirect('Perfil_Detail_Vicerrector')
    else:
        form = Perfil_Form_Vicerrector(instance=perfil)  
        return render(request, 'Vicerrector/Perfil/perfil_update_vicerrector.html', {'form': form})
    


#........................EVENTO.............................

@method_decorator([login_required, vicerrector_required], name='dispatch')
class Evento_List_Vicerrector(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "Vicerrector/eventos_vicer.html" 
    context_object_name = 'eventos'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related(
            'area', 'departamento', 'modalidad'  # Añade 'modalidad' aquí
        ).order_by('-fecha_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['areas'] = Area.objects.all().order_by('nombre_area')
        context['departamentos'] = Departamento.objects.select_related('area').order_by('nombre_departamento')
        
        # Consulta corregida para tipos de evento
        tipos_eventos = Evento.objects.values('tipo__nombre').annotate(
            count=Count('id')).order_by('tipo__nombre')
        context['tipos_eventos_json'] = json.dumps(
            [{'tipo': item['tipo__nombre'], 'count': item['count']} for item in tipos_eventos],
            cls=DjangoJSONEncoder
        )

        # Consulta corregida para modalidades (usando la relación)
        modalidad_eventos = Evento.objects.values('modalidad__nombre').annotate(
            count=Count('id')).order_by('modalidad__nombre')
        context['modalidad_eventos_json'] = json.dumps(
            [{'modalidad': item['modalidad__nombre'], 'count': item['count']} for item in modalidad_eventos],
            cls=DjangoJSONEncoder
        )
        
        return context


@method_decorator([login_required, vicerrector_required], name='dispatch')
class Evento_Detail_Vicerrector(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = "Vicerrector/evento_detail_vicerrector.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()
        # Add any additional context data here
        return context

#.......................................PREMIO................................................................
@method_decorator([login_required, vicerrector_required], name='dispatch')
class Premio_List_Vicerrector(LoginRequiredMixin, ListView):
    model = Premio
    template_name = "Vicerrector/premios_vicer.html"
    context_object_name = 'premios'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related('area', 'departamento').order_by('-fecha_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #optene a y depa
        context['areas'] = Area.objects.all().order_by('nombre_area')
        context['departamentos'] = Departamento.objects.select_related('area').order_by('nombre_departamento')
        
        # Calcular pendientes por area
        areas_pendientes = Premio.objects.filter(aprobacion='Pendiente').values(
            'area__nombre_area').annotate(count=Count('id'))
        context['areas_pendientes_json'] = json.dumps(list(areas_pendientes), cls=DjangoJSONEncoder)
        
        # Calcular por  area
        tipos_premios_por_area = Premio.objects.values(
            'area__nombre_area', 'tipo').annotate(
            count=Count('id')).order_by('area__nombre_area', 'tipo')
        context['tipos_premios_por_area_json'] = json.dumps(list(tipos_premios_por_area), cls=DjangoJSONEncoder)
        
        # Calculatr premios en general
        tipos_premios = Premio.objects.values('tipo').annotate(
            count=Count('id')).order_by('tipo')
        context['tipos_premios_json'] = json.dumps(list(tipos_premios), cls=DjangoJSONEncoder)
        
        return context
@method_decorator([login_required, vicerrector_required], name='dispatch')
class Premio_Detail_Vicerrector(LoginRequiredMixin, DetailView):
    model = Premio
    template_name = "Vicerrector/premio_detail_vicerrector.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        premio = self.get_object()
        # Add any additional context data here
        return context




@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Premio_Detail_Vicerrector(LoginRequiredMixin, DetailView):
    model = Premio
    template_name = "Vicerrector/premio_detail_vicerrector.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        premio = self.get_object()  
        premio_all = Premio.objects.all
        context['premio_all'] = premio_all  
        return context
    
#............................Articulo....................................................................

@method_decorator([login_required, vicerrector_required], name='dispatch')
class Articulo_List_Vicerrector(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "Vicerrector/articulos_vicer.html"
    context_object_name = 'articulos'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related(
            'area', 'departamento'
        ).prefetch_related('autores').order_by('-fecha_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all areas and departments for filters
        context['areas'] = Area.objects.all().order_by('nombre_area')
        context['departamentos'] = Departamento.objects.select_related('area').order_by('nombre_departamento')
        
        # Conteos optimizados
        conteos = Articulo.objects.aggregate(
            total_revistas=Count('id', filter=Q(doi__isnull=False) & ~Q(issn_isbn='')), 
            total_publicaciones=Count('id', filter=Q(volumen__isnull=False))
        )

        context.update({
            'revistas': conteos['total_revistas'] or 0,
            'publicaciones': conteos['total_publicaciones'] or 0,
            'conteos_por_area': self._get_conteos_por_area(),
            'conteos_por_areasafe': self._get_conteos_json()
        })
        
        return context

    def _get_conteos_por_area(self):
        return Area.objects.annotate(
            total=Count('articulo'),
            revistas=Count('articulo', filter=Q(articulo__doi__isnull=False) & ~Q(articulo__issn_isbn='')),
            publicaciones=Count('articulo', filter=Q(articulo__volumen__isnull=False))
        ).values('nombre_area', 'total', 'revistas', 'publicaciones')

    def _get_conteos_json(self):
        import json
        return json.dumps(list(self._get_conteos_por_area()))

@method_decorator([login_required, vicerrector_required], name='dispatch')
class Articulo_Detail_Vicerrector(LoginRequiredMixin, DetailView):
    model = Articulo
    template_name = "Vicerrector/articulo_detail_vicerrector.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articulo = self.get_object()
        
        context['Articulo_Revista'] = articulo.doi and articulo.issn.strip() != ''
        context['Articulo_Publicacion'] = articulo.volumen and articulo.capitulo.strip() != ''
        return context


#..............................Proyecto............................................................

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Proyecto_List_Vicerrector(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "Vicerrector/proyectos_vicer.html"
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular la cantidad de proyectos por estado
        estados_proyectos = Proyecto.objects.values('estado_proyecto').annotate(count=Count('id')).order_by('estado_proyecto')
        context['estados_proyectos_json'] = json.dumps(list(estados_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por departamento
        departamentos_proyectos = Proyecto.objects.values('departamento').annotate(count=Count('id')).order_by('departamento')
        context['departamentos_proyectos_json'] = json.dumps(list(departamentos_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por subtipo de proyecto
        subtipos_proyectos = Proyecto.objects.values('subtipo_proyecto').annotate(count=Count('id')).order_by('subtipo_proyecto')
        context['subtipos_proyectos_json'] = json.dumps(list(subtipos_proyectos), cls=DjangoJSONEncoder)
        
        sector_estrategico = Proyecto.objects.values('sector_estrategico').annotate(count=Count('id')).order_by('sector_estrategico')
        context['sector_estrategico'] = json.dumps(list(sector_estrategico), cls=DjangoJSONEncoder)
        
        return context


@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Proyecto_Detail_Vicerrector(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = "Vicerrector/proyecto_detail_vicerrector.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()  
        proyecto_all = Proyecto.objects.all
        context['proyecto_all'] = proyecto_all  
        return context
    
#.....................................Programa.......................................................

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Programa_List_Vicerrector(LoginRequiredMixin, ListView):
    model = Programa
    template_name = "Vicerrector/programas_vicer.html"
    context_object_name = 'programa'

 
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
         
        # Obtener programas filtrados
        programas_filtrados = self.get_queryset()
        context['programas_filtrados'] = programas_filtrados
        
        # Estadísticas generales
        context['total_programas'] = Programa.objects.count()
        context['programas_activos'] = Programa.objects.filter(
            aprobacion='Aprobado',
            fecha_fin__gte=date.today()  # Usar date.today() en lugar de datetime.now().date()
        ).count()

        context['total_entidades'] = EntidadParticipante.objects.count()
        
        # Opciones para filtros
        context['tipos_programa'] = TipoPrograma.objects.all()
        context['sectores_estrategicos'] = SectorEstrategico.objects.all()
        
        # Corregir obtención de años disponibles
        years = Programa.objects.filter(fecha_inicio__isnull=False).annotate(
            year=ExtractYear('fecha_inicio')
        ).values_list('year', flat=True).distinct().order_by('-year')
        context['years_disponibles'] = list(years)
        
        # Datos para gráficos
        context.update(self._get_chart_data())
        
        return context
    
    def _get_chart_data(self):
        """Generar datos para los gráficos"""
        
        # Programas por tipo
        tipos_programa = list(
            Programa.objects.values('tipo_programa__nombre')
            .annotate(count=Count('id'))
            .order_by('tipo_programa__nombre')
        )
        
        # Estados de aprobación
        estados_aprobacion = list(
            Programa.objects.values('aprobacion')
            .annotate(count=Count('id'))
            .order_by('aprobacion')
        )
        
        # Sectores estratégicos
        sector_estrategico = list(
            Programa.objects.values('sector_estrategico__nombre')
            .annotate(count=Count('id'))
            .order_by('sector_estrategico__nombre')
        )
        
        # CORRECCIÓN PRINCIPAL: Programas por año
        programas_por_ano = list(
            Programa.objects.filter(fecha_inicio__isnull=False)
            .annotate(year=ExtractYear('fecha_inicio'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )
        
        return {
            'tipos_programa_json': json.dumps(tipos_programa, cls=DjangoJSONEncoder),
            'estados_aprobacion_json': json.dumps(estados_aprobacion, cls=DjangoJSONEncoder),
            'sector_estrategico_json': json.dumps(sector_estrategico, cls=DjangoJSONEncoder),
            'programas_por_ano_json': json.dumps(programas_por_ano, cls=DjangoJSONEncoder),
        }    

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Programa_Detail_Vicerrector(LoginRequiredMixin, DetailView):
    model = Programa
    template_name = "Vicerrector/programa_detail_vicerrector.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programa = self.get_object()  
        programa_all = Programa.objects.all
        context['programa_all'] = programa_all  
        return context



@login_required
@vicerrector_required
def programa_estadisticas_api(request):
    """API para obtener estadísticas de programas"""
    
    # Estadísticas por estado
    stats_estado = dict(
        Programa.objects.values('aprobacion')
        .annotate(count=Count('id'))
        .values_list('aprobacion', 'count')
    )
    
    # Estadísticas por tipo
    stats_tipo = dict(
        Programa.objects.values('tipo_programa__nombre')
        .annotate(count=Count('id'))
        .values_list('tipo_programa__nombre', 'count')
    )
    
    # Programas activos vs inactivos
    fecha_actual = datetime.now().date()
    programas_activos = Programa.objects.filter(
        fecha_fin__gte=fecha_actual,
        aprobacion='Aprobado'
    ).count()
    
    programas_finalizados = Programa.objects.filter(
        fecha_fin__lt=fecha_actual
    ).count()
    
    return JsonResponse({
        'stats_estado': stats_estado,
        'stats_tipo': stats_tipo,
        'programas_activos': programas_activos,
        'programas_finalizados': programas_finalizados,
        'total_programas': Programa.objects.count()
    })


#...............................Investigador...................................

@method_decorator([login_required, vicerrector_required], name='dispatch')
class List_Investigador_Vicerrector(LoginRequiredMixin, ListView):
    model = Perfil
    template_name = 'Vicerrector/list_investigador_vicerrector.html'
    context_object_name = 'investigadores'
 

    def get_queryset(self):
        return Perfil.objects.select_related('area', 'departamento', 'categoria_docente').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Area.objects.all()
        context['categoria'] = Categoria_docente.objects.all()
        context['departamentos'] = Departamento.objects.select_related('area').order_by('nombre_departamento')
        return context
        


@method_decorator([login_required, vicerrector_required], name='dispatch')
class List_Investigador_Vicerrector_Usuario(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'Vicerrector/list_investigador_vicerrector_usuario.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        # Excluir usuarios con los roles de "vicerrector" y "admin"
        return Usuario.objects.select_related('area', 'departamento').exclude(rol__in=['Vicerrector', 'admin'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Area.objects.all()
        context['departamentos'] = Departamento.objects.select_related('area').order_by('nombre_departamento')
        return context

 
#.......................................................       
#.......................................................

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Curriculo_Investigador_Vicerrector(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        # Obtén el perfil del investigador basado en el ID proporcionado en la URL
        perfil_investigador = get_object_or_404(Perfil, pk=id)
        
        # Consultas para obtener los resultados académicos del investigador por tipo
        eventos = Evento.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        proyectos = Proyecto.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        programas = Programa.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        premios = Premio.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        articulos = Articulo.objects.filter(usuario=perfil_investigador.usuario).order_by('fecha_create')
        
        # Combina todas las consultas en una sola lista ordenada por fecha en orden ascendente
        resultados = sorted(chain(eventos, proyectos, programas, premios, articulos), key=lambda x: x.fecha_create)
        
        # Agregar 'nombre' y 'tipo_resultado' a cada resultado
        for resultado in resultados:
            if isinstance(resultado, Evento):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Evento'
            elif isinstance(resultado, Proyecto):
                resultado.nombre = resultado.nombre_proyecto
                resultado.tipo_resultado = 'Proyecto'
            elif isinstance(resultado, Programa):
                resultado.nombre = resultado.nombre_programa
                resultado.tipo_resultado = 'Programa'
            elif isinstance(resultado, Premio):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Premio'
            elif isinstance(resultado, Articulo):
                resultado.nombre = resultado.titulo
                resultado.tipo_resultado = 'Articulo'
        
        # Pasa los resultados a la plantilla
        return render(request, 'Vicerrector/curriculo_list_user_vicerrector.html', {'resultados': resultados, 'perfil_investigador': perfil_investigador})
    

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Informacion_Detail_Investigador_Vicerrector(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name = "Vicerrector/informacion_investigador_vicerrector.html"





@login_required
@permission_required('auth.change_user')
def CambiarRolVice(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    available_roles = obtener_roles_personalizados()
    
    if request.method == 'POST':
        nuevo_rol = request.POST.get('role')
        
      
        if nuevo_rol not in dict(ROLES_BASE):
            messages.error(request, 'Rol seleccionado no válido')
            return redirect('CambiarRol', id=usuario.id)
        
        usuario.rol = nuevo_rol
        usuario.save()
        
        messages.success(request, f'Rol actualizado exitosamente a {usuario.get_rol_display()}')
        return redirect('lista_usuarios')
    
    return render(request, "plataforma/CambiarRolVice.html", "plataforma/list_investigador.html", {
        'usuario': usuario,
        'available_roles': available_roles,
        'rol_actual': usuario.get_rol_display(),
    })

 
#>>>>>>>>>>>>>>>>>>>>>>>>>    Admin     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#.......................Revista_Libro_Conferencia....................................
@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Revista_Libro_Conferencia_Create(LoginRequiredMixin, CreateView):
    model = Revista_Libro_Conferencia
    form_class = Revista_Libro_Conferencia_Form
    template_name = "RevistaLibro/revista_libro_conferencia_create.html"
    success_url = reverse_lazy('Revista_Libro_Conferencia_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear la publicación. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Publicación creada exitosamente.")
        return super().form_valid(form)
   
class Revista_Libro_Conferencia_List(LoginRequiredMixin, ListView):
    model = Revista_Libro_Conferencia
    template_name = "RevistaLibro/revista_libro_conferencia_list.html" 
    context_object_name = 'objetos'
    
@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Revista_Libro_Conferencia_Detail(LoginRequiredMixin,  DetailView):
    model = Revista_Libro_Conferencia
    template_name = "RevistaLibro/revista_libro_conferencia_detail.html" 
    context_object_name = 'objeto'



@login_required
def Revista_Libro_Conferencia_Delete(request, id):
    publicacion = get_object_or_404(Revista_Libro_Conferencia, id=id)
    publicacion.delete()
    messages.success(request, "Publicación eliminada exitosamente.")
    return redirect("Revista_Libro_Conferencia_List")


@login_required
def Revista_Libro_Conferencia_Update(request, id):
    publicacion = get_object_or_404(Revista_Libro_Conferencia, pk=id) 
    if request.method == 'POST':
        form = Revista_Libro_Conferencia_Form(request.POST, instance=publicacion)  
        if form.is_valid():
            form.save()
            messages.success(request, "Publicación actualizada exitosamente.")
            return redirect('Revista_Libro_Conferencia_List')  
        else:
            messages.error(request, "Hubo un error al actualizar la publicación. Por favor, revisa los datos ingresados.")
    else:
        form = Revista_Libro_Conferencia_Form(instance=publicacion)  

    return render(request, 'RevistaLibro/revista_libro_conferencia_update.html', {'form': form})

#.......................Area....................................

@method_decorator([login_required, admin_staff_required], name='dispatch')
class Area_Create(LoginRequiredMixin, CreateView):
    model = Area
    form_class = Area_Form
    template_name = "Area/Area_create.html"
    success_url = reverse_lazy('Area_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el Area. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Area creada exitosamente.")
        return super().form_valid(form)   

@method_decorator([login_required, admin_staff_required], name='dispatch')
class Area_List(LoginRequiredMixin, ListView):
    model = Area
    template_name = "Area/Area_list.html" 
    context_object_name = 'Area'

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Area_Detail(LoginRequiredMixin, DetailView):
    model = Area
    template_name =  "Area/Area_detail.html" 
    context_object_name = 'Area'

    def get_queryset(self):
        return Area.objects.filter(usuario=self.request.user)


def Area_Delete(request, id):
    area = get_object_or_404(Area, id=id)
    area.delete()
    return redirect("Area_List")


def Area_Update(request, Area_id):
    area = get_object_or_404(Area, pk=Area_id) 
    if request.method == 'POST':
        form = Area_Form(request.POST, instance=area)  
        if form.is_valid():
            form.save()
            messages.success(request, "Área actualizada exitosamente.")
            return redirect('Area_List')  
    else:
        form = Area_Form(instance=area)  

    return render(request, 'Area/Area_update.html', {'form': form})


#Colaboradores
@method_decorator([login_required], name='dispatch')

class Colaboradores_Create(LoginRequiredMixin, CreateView):
    model = Colaborador
    form_class = Colaborador_Form
    template_name = "Colaboradores/Colaboradores_create.html"
    success_url = reverse_lazy('Colaboradores_List')

    def form_valid(self, form):
        # Asigna el usuario actual antes de guardar
        form.instance.usuario = self.request.user
        messages.success(self.request, "Colaborador creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el colaborador. Por favor, verifica los datos.")
        return super().form_invalid(form)


@method_decorator([login_required], name='dispatch')
class Colaboradores_List(LoginRequiredMixin, ListView):
    model = Colaborador
    template_name = "Colaboradores/Colaboradores_list.html"
    context_object_name = 'colaboradores'
    ordering = ['apellidos', 'nombre']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        # Staff, superusuario o Vicerrector ve todos
        if user.is_staff or user.is_superuser or hasattr(user, 'Vicerrector'):
            return queryset

        # Si no, solo los colaboradores del usuario autenticado
        return queryset.filter(usuario=user)
    

@method_decorator([login_required, admin_staff_required], name='dispatch')
class Colaboradores_Detail(LoginRequiredMixin, DetailView):
    model = Colaborador
    template_name = "Colaboradores/Colaboradores_detail.html"
    context_object_name = 'colaborador'

@method_decorator([login_required, admin_staff_required], name='dispatch')
class Colaboradores_Update(LoginRequiredMixin, UpdateView):
    model = Colaborador
    form_class = Colaborador_Form
    template_name = "Colaboradores/Colaboradores_update.html"
    success_url = reverse_lazy('Colaboradores_List')

    def form_valid(self, form):
        # Opcional: puedes verificar que el usuario sea el dueño del registro
        if form.instance.usuario != self.request.user and not self.request.user.is_superuser:
            messages.error(self.request, "No tienes permiso para editar este colaborador.")
            return redirect(self.success_url)
            
        messages.success(self.request, "Colaborador actualizado exitosamente.")
        return super().form_valid(form)

@method_decorator([login_required, admin_staff_required], name='dispatch')
def Colaboradores_Delete(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    # Verificar permisos
    if colaborador.usuario != request.user and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para eliminar este colaborador.")
        return redirect('Colaboradores_List')
    
    if request.method == 'POST':
        colaborador.delete()
        messages.success(request, "Colaborador eliminado exitosamente.")
        return redirect('Colaboradores_List')
    
    return render(request, 'Colaboradores/Colaboradores_confirm_delete.html', {'colaborador': colaborador})


# Vistas para TipoPremio
@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoPremio_Create(LoginRequiredMixin, CreateView):
    model = TipoPremio
    form_class = TipoPremioForm
    template_name = "TipoPremio/TipoPremio_create.html"
    success_url = reverse_lazy('TipoPremio_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el tipo de premio. Por favor, verifica los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Tipo de premio creado exitosamente.")
        print("Institución enviada:", form.cleaned_data.get('institucion'))
        return super().form_valid(form)


@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoPremio_List(LoginRequiredMixin, ListView):
    model = TipoPremio
    template_name = "TipoPremio/TipoPremio_list.html"
    context_object_name = 'tipos_premios'
    ordering = ['nombre']
    paginate_by = 10


@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoPremio_Detail(LoginRequiredMixin, DetailView):
    model = TipoPremio
    template_name = "TipoPremio/TipoPremio_detail.html"
    context_object_name = 'tipo_premio'


@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoPremio_Update(LoginRequiredMixin, UpdateView):
    model = TipoPremio
    form_class = TipoPremioForm
    template_name = "TipoPremio/TipoPremio_update.html"
    success_url = reverse_lazy('TipoPremio_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar el tipo de premio. Por favor, verifica los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Tipo de premio actualizado exitosamente.")
        return super().form_valid(form)


@login_required
@admin_staff_required
def TipoPremio_Delete(request, id):
    tipo_premio = get_object_or_404(TipoPremio, id=id)
    if request.method == 'POST':
        tipo_premio.delete()
        messages.success(request, "Tipo de premio eliminado exitosamente.")
        return redirect('TipoPremio_List')
    
    return render(request, 'TipoPremio/TipoPremio_confirm_delete.html', {'tipo_premio': tipo_premio})

# Vistas para CaracterPremio
@method_decorator([login_required, admin_staff_required], name='dispatch')
class CaracterPremio_Create(LoginRequiredMixin, CreateView):
    model = CaracterPremio
    form_class = CaracterPremioForm
    template_name = "CaracterPremio/CaracterPremio_create.html"
    success_url = reverse_lazy('CaracterPremio_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el carácter del premio. Por favor, verifica los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Carácter de premio creado exitosamente.")
        return super().form_valid(form)


@method_decorator([login_required, admin_staff_required], name='dispatch')
class CaracterPremio_List(LoginRequiredMixin, ListView):
    model = CaracterPremio
    template_name = "CaracterPremio/CaracterPremio_list.html"
    context_object_name = 'caracteres_premios'
    ordering = ['nombre']
    paginate_by = 10


@method_decorator([login_required, admin_staff_required], name='dispatch')
class CaracterPremio_Detail(LoginRequiredMixin, DetailView):
    model = CaracterPremio
    template_name = "CaracterPremio/CaracterPremio_detail.html"
    context_object_name = 'caracter_premio'


@method_decorator([login_required, admin_staff_required], name='dispatch')
class CaracterPremio_Update(LoginRequiredMixin, UpdateView):
    model = CaracterPremio
    form_class = CaracterPremioForm
    template_name = "CaracterPremio/CaracterPremio_update.html"
    success_url = reverse_lazy('CaracterPremio_List')

    def form_valid(self, form):
        messages.success(self.request, "Carácter de premio actualizado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el carácter de premio.")
        return super().form_invalid(form)


@login_required
@admin_staff_required
def CaracterPremio_Delete(request, id):
    caracter_premio = get_object_or_404(CaracterPremio, id=id)
    if request.method == 'POST':
        caracter_premio.delete()
        messages.success(request, "Carácter del premio eliminado exitosamente.")
        return redirect('CaracterPremio_List')
    
    return render(request, 'CaracterPremio/CaracterPremio_confirm_delete.html', {'caracter_premio': caracter_premio})


# Vistas para Modalidad
@method_decorator([login_required, admin_staff_required], name='dispatch')
class Modalidad_Create(LoginRequiredMixin, CreateView):
    model = Modalidad
    form_class = ModalidadForm
    template_name = "Modalidad/Modalidad_create.html"
    success_url = reverse_lazy('Modalidad_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear la modalidad. Por favor, verifica los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Modalidad creada exitosamente.")
        return super().form_valid(form)

@method_decorator([login_required, admin_staff_required], name='dispatch')
class Modalidad_List(LoginRequiredMixin, ListView):
    model = Modalidad
    template_name = "Modalidad/Modalidad_list.html"
    context_object_name = 'modalidades'
    ordering = ['nombre']
    paginate_by = 10

@method_decorator([login_required, admin_staff_required], name='dispatch')
class Modalidad_Detail(LoginRequiredMixin, DetailView):
    model = Modalidad
    template_name = "Modalidad/Modalidad_detail.html"
    context_object_name = 'modalidad'

@method_decorator([login_required, admin_staff_required], name='dispatch')
class Modalidad_Update(LoginRequiredMixin, UpdateView):
    model = Modalidad
    form_class = ModalidadForm
    template_name = "Modalidad/Modalidad_update.html"
    success_url = reverse_lazy('Modalidad_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar la modalidad. Por favor, verifica los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Modalidad actualizada exitosamente.")
        return super().form_valid(form)

@login_required
@admin_staff_required
def Modalidad_Delete(request, id):
    modalidad = get_object_or_404(Modalidad, id=id)
    if request.method == 'POST':
        modalidad.delete()
        messages.success(request, "Modalidad eliminada exitosamente.")
        return redirect('Modalidad_List')
    
    return render(request, 'Modalidad/Modalidad_confirm_delete.html', {'modalidad': modalidad})


@login_required
@admin_staff_required
def EventoBase_Delete(request, id):
    evento_base = get_object_or_404(EventoBase, id=id)
    if request.method == 'POST':
        evento_base.delete()
        messages.success(request, "Evento base eliminado exitosamente.")
        return redirect('EventoBase_List')
    
    return render(request, 'EventoBase/EventoBase_confirm_delete.html', {'evento_base': evento_base})

#....................... #CategoriaDocente....................................
@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CategoriaDocenteCreate(LoginRequiredMixin, CreateView):
    model = Categoria_docente
    form_class = CategoriaDocenteForm
    template_name = "Categorias/CategoriaDocente_create.html"
    success_url = reverse_lazy('CategoriaDocenteList')

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la categoría docente. Verifique los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Categoría docente creada exitosamente.")
        return super().form_valid(form)


@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CategoriaDocenteList(LoginRequiredMixin, ListView):
    model = Categoria_docente
    template_name = "Categorias/CategoriaDocente_List.html" 
    context_object_name = 'categorias_docentes'
    paginate_by = 10

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CategoriaDocenteDetail(LoginRequiredMixin, DetailView):
    model = Categoria_docente
    template_name = "Categorias/CategoriaDocente_detail.html" 
    context_object_name = 'categoria_docente'

@login_required
def CategoriaDocenteDelete(request, id):
    categoria = get_object_or_404(Categoria_docente, id=id)
    try:
        categoria.delete()
        messages.success(request, "Categoría docente eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar: {str(e)}")
    return redirect("CategoriaDocenteList")

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CategoriaDocenteUpdate(LoginRequiredMixin, UpdateView):
    model = Categoria_docente
    form_class = CategoriaDocenteForm
    template_name = "Categorias/CategoriaDocente_update.html"
    success_url = reverse_lazy('CategoriaDocenteList')

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la categoría docente.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Categoría docente actualizada exitosamente.")
        return super().form_valid(form)






#bASE DE DATOS 



@method_decorator([login_required, vicerrector_required], name='dispatch') 
class BasesDatosCreate(LoginRequiredMixin, CreateView):
    model = Indexacion
    form_class = BasesDatosForm
    template_name = "BasesDatos/BasesDatos_create.html"
    success_url = reverse_lazy('BasesDatosList')

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la base de datos. Verifique los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Base de datos creada exitosamente.")
        return super().form_valid(form)

@method_decorator([login_required, vicerrector_required], name='dispatch')   
class BasesDatosList(LoginRequiredMixin, ListView):
    model = Indexacion
    template_name = "BasesDatos/BasesDatos_List.html" 
    context_object_name = 'bases_datos'
    paginate_by = 10

@method_decorator([login_required, vicerrector_required], name='dispatch')   
class BasesDatosDetail(LoginRequiredMixin, DetailView):
    model = Indexacion
    template_name = "BasesDatos/BasesDatos_detail.html" 
    context_object_name = 'base_datos'

@method_decorator([login_required, vicerrector_required], name='dispatch')   
class BasesDatosUpdate(LoginRequiredMixin, UpdateView):
    model = Indexacion
    form_class = BasesDatosForm
    template_name = "BasesDatos/BasesDatos_update.html"
    success_url = reverse_lazy('BasesDatosList')

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la base de datos. Verifique los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Base de datos actualizada exitosamente.")
        return super().form_valid(form)

@login_required
def BasesDatosDelete(request, id):
    base_datos = get_object_or_404(Indexacion, id=id)
    try:
        base_datos.delete()
        messages.success(request, "Base de datos eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar: {str(e)}")
    return redirect("BasesDatosList")


#....................... #CategoriaCientifica....................................

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CategoriaCientificaCreate(LoginRequiredMixin, CreateView):
    model = Categoria_cientifica
    form_class = CategoriaCientificaForm
    template_name = "Categorias/CategoriaCientifica_create.html"
    success_url = reverse_lazy('CategoriaCientificaList')

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la categoría científica. Verifique los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Categoría científica creada exitosamente.")
        return super().form_valid(form)

@method_decorator([login_required, vicerrector_required ], name='dispatch')   
class CategoriaCientificaList(LoginRequiredMixin, ListView):
    model = Categoria_cientifica
    template_name = "Categorias/CategoriaCientifica_List.html" 
    context_object_name = 'categorias_cientificas'
    paginate_by = 10

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CategoriaCientificaDetail(LoginRequiredMixin, DetailView):
    model = Categoria_cientifica
    template_name = "Categorias/CategoriaCientifica_detail.html" 
    context_object_name = 'categoria_cientifica'

def CategoriaCientificaDelete(request, id):
    categoria = get_object_or_404(Categoria_cientifica, id=id)
    try:
        categoria.delete()
        messages.success(request, "Categoría científica eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar: {str(e)}")
    return redirect("CategoriaCientificaList")

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CategoriaCientificaUpdate(LoginRequiredMixin, UpdateView):
    model = Categoria_cientifica
    form_class = CategoriaCientificaForm 
    template_name = "Categorias/CategoriaCientifica_update.html"
    success_url = reverse_lazy('CategoriaCientificaList')

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la categoría científica.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Categoría científica actualizada exitosamente.")
        return super().form_valid(form)



#.......................Departamento....................................

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Departamento_Create(LoginRequiredMixin, CreateView):
    model = Departamento
    form_class = Departamento_Form
    template_name = "Departamento/Departamento_create.html"
    success_url = reverse_lazy('Departamento_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el Departamento. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Departamento creado exitosamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Area.objects.all()
        return context

        
@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Departamento_List(LoginRequiredMixin, ListView):
    model = Departamento
    template_name = "Departamento/Departamento_list.html" 
    context_object_name = 'Departamento'

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Departamento_Detail(LoginRequiredMixin, DetailView):
    model = Departamento
    template_name =  "Departamento/Departamento_detail.html" 
    context_object_name = 'Departamento'

    def get_queryset(self):
        return Departamento.objects.filter(usuario=self.request.user)



def Departamento_Delete(request, id):
    departamento = get_object_or_404(Departamento, id=id)
    departamento.delete()
    return redirect("Departamento_List")


def Departamento_Update(request, id):
    departamento = get_object_or_404(Departamento, id=id)
    
    if request.method == 'POST':
        form = Departamento_Form(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento actualizado exitosamente.")
            return redirect('Departamento_List')
        else:
            messages.error(request, "Error al actualizar. Verifique los datos.")
    else:
        form = Departamento_Form(instance=departamento)
    
    # Asegúrate de pasar el objeto departamento al contexto
    return render(request, 'Departamento/Departamento_update.html', {
        'form': form,
        'departamento': departamento  # Esto es importante para los campos manuales
    })

#.......................CarcterEvento....................................
@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CarcterEvento_Create(LoginRequiredMixin, CreateView):
    model = CarcterEvento
    form_class = CarcterEvento_Form
    template_name = "CarcterEvento/CarcterEvento_create.html"
    success_url = reverse_lazy('CarcterEvento_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el caracter de evento. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Cracter creado exitosamente.")
        return super().form_valid(form)

@method_decorator([login_required, vicerrector_required ], name='dispatch')    
class CarcterEvento_List(LoginRequiredMixin, ListView):
    model = CarcterEvento
    template_name = "CarcterEvento/CarcterEvento_list.html" 
    context_object_name = 'CarcterEvento'


@method_decorator([login_required, vicerrector_required ], name='dispatch')
class CarcterEvento_Detail(LoginRequiredMixin, DetailView):
    model = CarcterEvento
    template_name =  "CarcterEvento/CarcterEvento_detail.html" 
    context_object_name = 'CarcterEvento'

    def get_queryset(self):
        return CarcterEvento.objects.filter(usuario=self.request.user)


@login_required
def CarcterEvento_Delete(request, id):
    caracterevento= get_object_or_404(CarcterEvento, id=id)
    caracterevento.delete()
    return redirect("CarcterEvento_List")

@login_required
def CarcterEvento_Update(request, CarcterEvento_id):
    caracterevento = get_object_or_404(CarcterEvento, pk=CarcterEvento_id) 
    if request.method == 'POST':
        form = CarcterEvento_Form(request.POST, instance=caracterevento)  # Fixed variable name
        if form.is_valid():
            form.save()
            messages.success(request, "Característica actualizada exitosamente.")
            return redirect('CarcterEvento_List')  
    else:
        form = CarcterEvento_Form(instance=caracterevento)  # Fixed variable name

    return render(request, 'CarcterEvento/CarcterEvento_update.html', {
        'form': form,
        'caracterevento': caracterevento  # Passing the object to template
    })

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


#.......................Cargo....................................

@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Cargo_Create(LoginRequiredMixin, CreateView):
    model = Cargo
    form_class = Cargo_Form
    template_name = "Cargo/cargo_create.html"
    success_url = reverse_lazy('Cargo_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el cargo. Por favor, intenta de nuevo.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Cracter creado exitosamente.")
        return super().form_valid(form)
    

@method_decorator([login_required, vicerrector_required ], name='dispatch')    
class Cargo_List(LoginRequiredMixin, ListView):
    model = Cargo
    template_name = "Cargo/cargo_list.html" 
    context_object_name = 'Cargo'


@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Cargo_Detail(LoginRequiredMixin, DetailView):
    model = Cargo
    template_name =  "Cargo/cargo_detail.html" 
    context_object_name = 'Cargo'

    def get_queryset(self):
        return Cargo.objects.filter(usuario=self.request.user)


@login_required
def Cargo_Delete(request, id):
    cargo= get_object_or_404(Cargo, id=id)
    cargo.delete()
    return redirect("Cargo_List")


@login_required
def Cargo_Update(request, pk):  # Recibes el parámetro pk de la URL
    # Usa pk directamente en lugar de Cargo_id
    cargo = get_object_or_404(Cargo, pk=pk)  # Corregido aquí
    
    if request.method == 'POST':
        form = Cargo_Form(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo actualizado exitosamente.")
            return redirect('Cargo_List')
    else:
        form = Cargo_Form(instance=cargo)

    return render(request, 'Cargo/cargo_update.html', {'form': form})

##.......................Admin....................................

@method_decorator([login_required, pure_admin_required], name='dispatch')
class Evento_List_Admin(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "Plataforma/General/eventos_admin.html" 
    context_object_name = 'eventos'  # Cambiado a plural para reflejar que es una lista
    def get_queryset(self):
        return Evento.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calcular tipos de eventos en general (regional, nacional, internacional)
        tipos_eventos = Evento.objects.values('tipo').annotate(
            count=Count('id')).order_by('tipo')
        context['tipos_eventos_json'] = json.dumps(list(tipos_eventos), cls=DjangoJSONEncoder)
        return context  # Asegúrate de devolver el contexto
      
        
@method_decorator([login_required, pure_admin_required ], name='dispatch')
class Evento_Detail_Admin(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = "Plataforma/General/evento_detail_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()  
        evento_all = Evento.objects.all
        context['evento_all'] = evento_all  
        return context

@method_decorator([login_required, pure_admin_required ], name='dispatch')
class Premio_List_Admin(LoginRequiredMixin, ListView):
    model = Premio
    template_name = "Plataforma/General/premios_admin.html"
    context_object_name = 'premio'

    def get_queryset(self):
        return Premio.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular pendientes por area
        areas_pendientes = Premio.objects.filter(aprobacion='Pendiente').values(
            'area__nombre_area').annotate(count=Count('id'))
        context['areas_pendientes_json'] = json.dumps(list(areas_pendientes), cls=DjangoJSONEncoder)
        
        # Calcular por  area
        tipos_premios_por_area = Premio.objects.values(
            'area__nombre_area', 'tipo').annotate(
            count=Count('id')).order_by('area__nombre_area', 'tipo')
        context['tipos_premios_por_area_json'] = json.dumps(list(tipos_premios_por_area), cls=DjangoJSONEncoder)
        
        # Calculatr premios en general
        tipos_premios = Premio.objects.values('tipo').annotate(
            count=Count('id')).order_by('tipo')
        context['tipos_premios_json'] = json.dumps(list(tipos_premios), cls=DjangoJSONEncoder)
        
        return context
@method_decorator([login_required, pure_admin_required ], name='dispatch')  
class Premio_Detail_Admin(LoginRequiredMixin, DetailView):
    model = Premio
    template_name = "Plataforma/General/premio_detail_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        premio = self.get_object()  
        premio_all = Premio.objects.all
        context['premio_all'] = premio_all  
        return context

# Vistas para TipoEvento
@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoEvento_Create(LoginRequiredMixin, CreateView):
    model = TipoEvento
    form_class = TipoEventoForm
    template_name = "TipoEvento/TipoEvento_create.html"
    success_url = reverse_lazy('TipoEvento_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el tipo de evento. Por favor, verifica los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Tipo de evento creado exitosamente.")
        return super().form_valid(form)

@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoEvento_List(LoginRequiredMixin, ListView):
    model = TipoEvento
    template_name = "TipoEvento/TipoEvento_list.html"
    context_object_name = 'tipos_evento'
    ordering = ['nombre']
    paginate_by = 10

@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoEvento_Detail(LoginRequiredMixin, DetailView):
    model = TipoEvento
    template_name = "TipoEvento/TipoEvento_detail.html"
    context_object_name = 'tipo_evento'

@method_decorator([login_required, admin_staff_required], name='dispatch')
class TipoEvento_Update(LoginRequiredMixin, UpdateView):
    model = TipoEvento
    form_class = TipoEventoForm
    template_name = "TipoEvento/TipoEvento_update.html"
    success_url = reverse_lazy('TipoEvento_List')

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar el tipo de evento. Por favor, verifica los datos.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Tipo de evento actualizado exitosamente.")
        return super().form_valid(form)

@login_required
@admin_staff_required
def TipoEvento_Delete(request, id):
    tipo_evento = get_object_or_404(TipoEvento, id=id)
    if request.method == 'POST':
        tipo_evento.delete()
        messages.success(request, "Tipo de evento eliminado exitosamente.")
        return redirect('TipoEvento_List')
    
    return render(request, 'TipoEvento/TipoEvento_confirm_delete.html', {'tipo_evento': tipo_evento})

@method_decorator([login_required, pure_admin_required], name='dispatch')
class Articulo_List_Admin(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "Plataforma/General/articulos_admin.html"
    context_object_name = 'articulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Conteo de revistas y publicaciones
        revistas = Articulo.objects.exclude(doi__exact='').exclude(doi__isnull=True).count()
        publicaciones = Articulo.objects.filter(Q(doi__exact='') | Q(doi__isnull=True)).count()

        # Agregar los conteos al contexto
        context['revistas'] = revistas
        context['publicaciones'] = publicaciones

        # Obtener todas las areas desde la base de datos
        areas = Area.objects.all()
        conteos_por_area = []

        for area in areas:
            total_articulos = Articulo.objects.filter(area=area).count()
            revistas_area = Articulo.objects.filter(area=area).exclude(doi__exact='').exclude(doi__isnull=True).count()
            publicaciones_area = total_articulos - revistas_area

            conteos_por_area.append({
                'area': area.nombre_area,  
                'total': total_articulos,
                'revistas': revistas_area,
                'publicaciones': publicaciones_area
            })

        context['conteos_por_area'] = conteos_por_area

        return context    
@method_decorator([login_required, pure_admin_required ], name='dispatch')
class Articulo_Detail_Admin(LoginRequiredMixin, DetailView):
    model = Articulo
    template_name =  "Plataforma/General/articulo_detail_admin.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articulo = self.get_object()
        Articulo.objects.all
    #Variables para controlar qué formularios mostrar
        context['Articulo_Revista'] = articulo.doi and articulo.issn.strip()!= ''#Variables para controlar qué formularios mostrar
        context['Articulo_Publicacion'] = articulo.volumen and articulo.capitulo.strip()!= ''
        return context
    
@method_decorator([login_required, pure_admin_required ], name='dispatch') 
class Proyecto_List_Admin(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "Plataforma/General/proyectos_admin.html"
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular la cantidad de proyectos por estado
        estados_proyectos = Proyecto.objects.values('estado_proyecto').annotate(count=Count('id')).order_by('estado_proyecto')
        context['estados_proyectos_json'] = json.dumps(list(estados_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por departamento
        departamentos_proyectos = Proyecto.objects.values('departamento').annotate(count=Count('id')).order_by('departamento')
        context['departamentos_proyectos_json'] = json.dumps(list(departamentos_proyectos), cls=DjangoJSONEncoder)
        
        # Calcular la cantidad de proyectos por subtipo de proyecto
        subtipos_proyectos = Proyecto.objects.values('subtipo_proyecto').annotate(count=Count('id')).order_by('subtipo_proyecto')
        context['subtipos_proyectos_json'] = json.dumps(list(subtipos_proyectos), cls=DjangoJSONEncoder)
        
        sector_estrategico = Proyecto.objects.values('sector_estrategico').annotate(count=Count('id')).order_by('sector_estrategico')
        context['sector_estrategico'] = json.dumps(list(sector_estrategico), cls=DjangoJSONEncoder)
        
        return context

@method_decorator([login_required, pure_admin_required ], name='dispatch')
class Proyecto_Detail_Admin(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = "Plataforma/General/proyecto_detail_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()  
        proyecto_all = Proyecto.objects.all
        context['proyecto_all'] = proyecto_all  
        return context
    
@method_decorator([login_required, pure_admin_required ], name='dispatch')
class Programa_List_Admin(LoginRequiredMixin, ListView):
    model = Programa
    template_name = "Plataforma/General/programas_admin.html"
    context_object_name = 'programa'

    def get_queryset(self):
        return Programa.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        
        sector_estrategico = Programa.objects.values('sector_estrategico').annotate(count=Count('id')).order_by('sector_estrategico')
        context['sector_estrategico'] = json.dumps(list(sector_estrategico), cls=DjangoJSONEncoder)
        
        return context

@method_decorator([login_required, pure_admin_required ], name='dispatch')
class Programa_Detail_Admin(LoginRequiredMixin, DetailView):
    model = Programa
    template_name = "Plataforma/General/programa_detail_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programa = self.get_object()  
        programa_all = Programa.objects.all
        context['programa_all'] = programa_all  
        return context
    
