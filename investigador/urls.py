from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views_marcadores
from .views_marcadores import (
    Evento_Create,
    Evento_List_Investigador,
    Evento_Detail_Investigador,
    Evento_Delete_Investigador,
    Evento_Update_Investigador,

    Proyecto_Create,
    Proyecto_List_Investigador,
    Proyecto_Detail_Investigador,
    Proyecto_Delete_Investigador,
    Proyecto_Update_Investigador,

    Programa_Create,
    Programa_List_Investigador,
    Programa_Detail_Investigador,
    Programa_Delete_Investigador,
    Programa_Update_Investigador,

    Premio_Create,
    Premio_List_Investigador,
    Premio_Detail_Investigador,
    Premio_Delete_Investigador,
    Premio_Update_Investigador,

    Perfil_Create_Investigador,
    Perfil_Detail_Investigador,
    Perfil_Update_Investigador,

    Articulo_Publicacion_Create,
    ArticuloCreate,
    Articulo_List_Investigador,
    Articulo_Detail_Investigador,
    Articulo_Delete_Investigador,
    Articulo_Publicacion_Update_Investigador,
    Articulo_Revista_Update_Investigador,
    buscar_autores,

    Curriculo_List_Investigador,
    Dashboard_Investigador,
    Evento_List,
    Premio_List,
    Articulo_List,
    Proyecto_List,
    api_usuarios,
    lista_notificaciones, 
    eliminar_notificacion, 
    eliminar_todas_notificaciones, 
    marcar_notificacion_leida, 
    marcar_todas_leidas, 
    obtener_contador_notificaciones, 
    ver_notificacion, 
    cambiar_estado_desde_notificacion,
    api_crear_colaborador,
    api_crear_revista_libro,
    obtener_institucion_tipo_premio,
    tipo_premio_create_ajax, crear_caracter_premio,
    crear_institucion_ajax, crear_colaborador_ajax, api_tipos_premio,
    buscar_entidades,
    TipoParticipacionList, crear_entidad
)

from .api_views import (api_entidades_search, api_tipos_participacion, api_usuarios_search, crear_entidad_ajax, crear_tipo_participacion_ajax, 
                        api_departamentos_por_area, api_usuarios_por_departamento)
from .api import EventoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/Evento', EventoViewSet, 'Evento')

urlpatterns = [
    # API usuarios
    path('api_usuarios/', api_usuarios, name='api_usuarios'),
    #ApI PROGRAMS
    path('ajax/crear-entidad/', crear_entidad, name='ajax_crear_entidad'),
    path('api/tipo_participacion/', TipoParticipacionList.as_view(), name='api_tipo_participacion'),
    path('api_entidades_search/', api_entidades_search, name='api_entidades_search'),
    path('api_tipos_participacion/', api_usuarios_search, name='api_tipos_participacion'),
    path('api_usuarios_search/', api_tipos_participacion, name='api_usuarios_search'),  
    path('crear_entidad_ajax/', crear_entidad_ajax, name='crear_entidad_ajax'), 
    path('crear_tipo_participacion_ajax/', crear_tipo_participacion_ajax, name='crear_tipo_participacion_ajax'),   
    path('api_departamentos_por_area/', api_departamentos_por_area, name='api_departamentos_por_area'),  
    path('api_usuarios_por_departamento/', api_usuarios_por_departamento, name='api_usuarios_por_departamento'),
    path('tipo-premio/create/ajax/', tipo_premio_create_ajax, name='TipoPremio_Create'),
    path('api/tipos-premio/', api_tipos_premio, name='api_tipos_premio'),
    path('caracter-premio/crear/', crear_caracter_premio, name='CaracterPremio_Create'),
    path('institucion/create/ajax/', crear_institucion_ajax, name='crear_institucion_ajax'),
    path('colaborador/create/ajax/', crear_colaborador_ajax, name='crear_colaborador_ajax'),

    # Notificaciones
    path('notificaciones/', lista_notificaciones, name='lista_notificaciones'),
    path('notificaciones/eliminar/<int:notificacion_id>/', eliminar_notificacion, name='eliminar_notificacion'),
    path('notificaciones/eliminar-todas/', eliminar_todas_notificaciones, name='eliminar_todas_notificaciones'),
    path('notificaciones/marcar-leida/<int:notificacion_id>/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificaciones/marcar-todas-leidas/', marcar_todas_leidas, name='marcar_todas_leidas'),
    path('notificaciones/contador/', obtener_contador_notificaciones, name='obtener_contador_notificaciones'),
    path('notificaciones/ver/<int:notificacion_id>/', ver_notificacion, name='ver_notificacion'),
    path('notificaciones/cambiar-estado/<int:notificacion_id>/', cambiar_estado_desde_notificacion, name='cambiar_estado_desde_notificacion'),

    # Evento 
    path('Evento_Create/', Evento_Create.as_view(), name='Evento_Create'),
    path('Evento_List_Investigador/', Evento_List_Investigador.as_view(), name='Evento_List_Investigador'),
    path('Evento_Detail_Investigador/<int:pk>/', Evento_Detail_Investigador.as_view(), name='Evento_Detail_Investigador'),
    path('Evento_Delete_Investigador/<int:id>/', Evento_Delete_Investigador, name="Evento_Delete_Investigador"),
    path('Evento_Update_Investigador/<int:evento_id>/', Evento_Update_Investigador, name='Evento_Update_Investigador'),

    path('configuracion/eventos-base/', views_marcadores.EventoBaseListView.as_view(), name='evento_base_list'),
    path('configuracion/eventos-base/crear/', views_marcadores.EventoBaseCreateView.as_view(), name='evento_base_create'),
    path('configuracion/eventos-base/editar/<int:pk>/', views_marcadores.EventoBaseUpdateView.as_view(), name='evento_base_update'),
    path('configuracion/eventos-base/eliminar/<int:pk>/', views_marcadores.EventoBaseDeleteView.as_view(), name='evento_base_delete'),
    
    # APIs para autocompletado
    path('api_eventos_base/', views_marcadores.api_eventos_base, name='api_eventos_base'),
    path('api_crear_evento_base/', views_marcadores.api_crear_evento_base, name='api_crear_evento_base'),
    path('api_crear_colaborador/', api_crear_colaborador, name='api_crear_colaborador'),
    path('api_crear_revista_libro/', api_crear_revista_libro, name='api_crear_revista_libro'),
    path('api/tipo-premio/<int:tipo_id>/', obtener_institucion_tipo_premio, name='obtener_institucion_tipo'),
    path("ajax/entidades/", buscar_entidades, name="ajax_entidades"),

    # Proyecto 
    path('Proyecto_Create/', Proyecto_Create.as_view(), name='Proyecto_Create'),
    path('Proyecto_List_Investigador/', Proyecto_List_Investigador.as_view(), name='Proyecto_List_Investigador'),
    path('Proyecto_Detail_Investigador/<int:pk>/', Proyecto_Detail_Investigador.as_view(), name='Proyecto_Detail_Investigador'),
    path('Proyecto_Delete_Investigador/<int:id>/', Proyecto_Delete_Investigador, name="Proyecto_Delete_Investigador"),
    path('Proyecto_Update_Investigador/<int:proyecto_id>/', Proyecto_Update_Investigador, name='Proyecto_Update_Investigador'),

    # Programa 
    path('Programa_Create/', Programa_Create.as_view(), name='Programa_Create'),
    path('Programa_List_Investigador/', Programa_List_Investigador.as_view(), name='Programa_List_Investigador'),
    path('Programa_Detail_Investigador/<int:pk>/', Programa_Detail_Investigador.as_view(), name='Programa_Detail_Investigador'),
    path('Programa_Delete_Investigador/<int:id>/', Programa_Delete_Investigador, name="Programa_Delete_Investigador"),
    path('Programa_Update_Investigador/<int:programa_id>/', Programa_Update_Investigador, name='Programa_Update_Investigador'),

    # Premio
    path('Premio_Create/', Premio_Create.as_view(), name='Premio_Create'),
    path('Premio_List_Investigador/', Premio_List_Investigador.as_view(), name='Premio_List_Investigador'),
    path('Premio_Detail_Investigador/<int:pk>/', Premio_Detail_Investigador.as_view(), name='Premio_Detail_Investigador'),
    path('Premio_Delete_Investigador/<int:id>/', Premio_Delete_Investigador, name="Premio_Delete_Investigador"),
    path('Premio_Update_Investigador/<int:premio_id>/', Premio_Update_Investigador, name='Premio_Update_Investigador'),
    
    # Perfil
    path('Perfil_Create_Investigador/', Perfil_Create_Investigador.as_view(), name='Perfil_Create_Investigador'),
    path('Perfil_Detail_Investigador/', Perfil_Detail_Investigador.as_view(), name='Perfil_Detail_Investigador'),
    path('Perfil_Update_Investigador/<int:perfil_id>/', Perfil_Update_Investigador, name='Perfil_Update_Investigador'),

    # Articulo
    path('buscar-autores/', buscar_autores, name='buscar_autores'),
    path('Articulo_Publicacion_Create/', Articulo_Publicacion_Create.as_view(), name='Articulo_Publicacion_Create'),
    path('Articulo_Revista_Create/', ArticuloCreate.as_view(), name='Articulo_Revista_Create'),
    path('Articulo_List_Investigador/', Articulo_List_Investigador.as_view(), name='Articulo_List_Investigador'),
    path('Articulo_Detail_Investigador/<int:pk>/', Articulo_Detail_Investigador.as_view(), name='Articulo_Detail_Investigador'),
    path('Articulo_Delete_Investigador/<int:id>/', Articulo_Delete_Investigador, name="Articulo_Delete_Investigador"),
    path('Articulo_Publicacion_Update_Investigador/<int:articulo_id>/', Articulo_Publicacion_Update_Investigador, name='Articulo_Publicacion_Update_Investigador'),
    path('Articulo_Revista_Update_Investigador/<int:articulo_id>/', Articulo_Revista_Update_Investigador, name='Articulo_Revista_Update_Investigador'),

    # Curriculo
    path('Curriculo_List_Investigador/', Curriculo_List_Investigador.as_view(), name='Curriculo_List_Investigador'),

    # Dashboard 
    path('Dashboard_Investigador/', Dashboard_Investigador.as_view(), name='Dashboard_Investigador'),
    path('Proyecto_List/', Proyecto_List.as_view(), name='Proyecto_List'),
    path('Articulo_List/', Articulo_List.as_view(), name='Articulo_List'),
    path('Premio_List/', Premio_List.as_view(), name='Premio_List'),
    path('Evento_List/', Evento_List.as_view(), name='Evento_List'),
]

# Añade las URLs de la API
urlpatterns += router.urls