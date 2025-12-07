from django.urls import path
from plataforma import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from usuarios.api import UsuarioViewSet

from .views import ( Perfil_Create_JefeArea, Perfil_Detail_JefeArea, Perfil_Update_JefeArea, LineaInvestigacion_Create,
                    LineaInvestigacion_Delete, LineaInvestigacion_List, LineaInvestigacion_Update,

                    Articulo_List_JefeArea, Articulo_Delete_JefeArea, Articulo_Detail_JefeArea, Cambiar_Estado_Articulo,
                    
                    Premio_List_JefeArea, Premio_Detail_JefeArea, Premio_Delete_JefeArea, Cambiar_Estado_Premio,
                    
                    Proyecto_List_JefeArea, Proyecto_Detail_JefeArea, Proyecto_Delete_JefeArea, Cambiar_Estado_Proyecto,
                    

                    Programa_List_JefeArea, Programa_Detail_JefeArea, Programa_Delete_JefeArea, Cambiar_Estado_Programa,
                    

                    Evento_List_JefeArea, Evento_Detail_JefeArea, Evento_Delete_JefeArea, Cambiar_Estado_Evento,
                    

                    Informacion_Detail_Investigador_Area, CambiarRolJefeArea,
                    List_Investigador_JefeArea,
                    List_Investigador_JefeArea_usuario, 
                    Curriculo_Investigador_JefeArea,

                    Dashboard_JefeArea, 

                    Proyecto_List_Areas,
                    Articulo_List_Areas,
                    Evento_List_Areas,
                    Premio_List_Areas,

              

                    Perfil_Create_JefeDepartamento, 
                    Perfil_Detail_JefeDepartamento, 
                    Perfil_Update_JefeDepartamento,

                    Articulo_List_Departamento, 
                    Articulo_Delete_JefeDepartamento, 
                    Articulo_Detail_JefeDepartamento, 
                    

                    Premio_List_Departamento,
                    Premio_Detail_JefeDepartamento, 
                    Premio_Delete_JefeDepartamento,
                    

                    Proyecto_List_Departamento, 
                    Proyecto_Detail_JefeDepartamento,
                    Proyecto_Delete_JefeDepartamento,
                    

                    Programa_List_JefeDepartamento,
                    Programa_Detail_JefeDepartamento, 
                    Programa_Delete_JefeDepartamento,
                    

                    Evento_List_JefeDepartamento, 
                    Evento_Detail_JefeDepartamento, 
                    Evento_Delete_JefeDepartamento,
                    

                    Informacion_Detail_Investigador_Departamento,
                    List_Investigador_JefeDepartamento, 
                    Curriculo_Investigador_Departamento,

                    Dashboard_JefeDepartamento, 
                    Proyecto_List_JefeDepartamento,
                    Articulo_List_JefeDepartamento,
                    Evento_List_JefeDepartamento,
                    Premio_List_JefeDepartamento, 
                    Proyecto_List_Vicerrector,  Articulo_List_Vicerrector, CambiarRolVicerrector, Premio_List_Vicerrector, 
                    Evento_List_Vicerrector,
                    Programa_List_Vicerrector,
                    List_Investigador_Vicerrector,
                    List_Investigador_Vicerrector_Usuario,
                    Curriculo_Investigador_Vicerrector,
                    Informacion_Detail_Investigador_Vicerrector, 
                    Dashboard_Vicerrector, 
                    Articulo_Detail_Vicerrector,
                    Programa_Detail_Vicerrector,
                    Proyecto_Detail_Vicerrector,
                    Premio_Detail_Vicerrector,
                    Evento_Detail_Vicerrector,
                    Perfil_Create_Vicerrector,
                    Perfil_Detail_Vicerrector,
                    Perfil_Update_Vicerrector,

                    Evento_List_Admin,
                    Premio_List_Admin,
                    Articulo_List_Admin,
                    Proyecto_List_Admin,
                    Programa_List_Admin,
                    Articulo_Detail_Admin, 
                    Programa_Detail_Admin,
                    Proyecto_Detail_Admin,
                    Premio_Detail_Admin,
                    Evento_Detail_Admin,
                    Dashboard_Admin, 

                    Area_Create, 
                    Area_List, 
                    Area_Detail, 
                    Area_Delete, 
                    Area_Update, 

                    Departamento_Create,
                    Departamento_List,
                    Departamento_Detail,
                    Departamento_Delete,
                    Departamento_Update,
                    editar_nombres_roles,
                    CategoriaDocenteCreate,
                    CategoriaDocenteList,
                    CategoriaDocenteDetail,
                    CategoriaDocenteUpdate,
                    CategoriaCientificaUpdate,
                    CategoriaDocenteDelete,

                    CategoriaCientificaCreate,
                    CategoriaCientificaList,
                    CategoriaCientificaDetail,
                    CategoriaCientificaDelete,
                    CategoriaCientificaUpdate, 
                    CambiarRol, ListaUsuarios, 
                    CarcterEvento_Create, CarcterEvento_List, CarcterEvento_Detail, CarcterEvento_Delete, CarcterEvento_Update, 
                    Cargo_Create, Cargo_List, Cargo_Detail, Cargo_Delete, Cargo_Update, ReporteCompletoView, api_revistas,
                    BasesDatosCreate, BasesDatosList, BasesDatosDetail, BasesDatosUpdate, BasesDatosDelete, Colaboradores_Delete, 
                    Colaboradores_Update, Colaboradores_Detail, Colaboradores_List, Colaboradores_Create, api_dashboard_data
)

router = routers.DefaultRouter()
router.register('api/Usuarios', UsuarioViewSet,'Usuarios')



urlpatterns = [
    path('reporte/', ReporteCompletoView.as_view(), name='reporte'),
    path('ListaUsuarios/',login_required (views.ListaUsuarios), name="ListaUsuarios"),
    path('usuario-autocomplete/', views.UsuarioAutocomplete.as_view(), name='usuario-autocomplete'),
    path('api_revistas/', views.api_revistas, name='api_revistas'),
#..................Area Departamento...........................

    path('revista-libro-conferencia/crear/', views.Revista_Libro_Conferencia_Create.as_view(), name='Revista_Libro_Conferencia_Create'),
    path('revista-libro-conferencia/lista/', views.Revista_Libro_Conferencia_List.as_view(), name='Revista_Libro_Conferencia_List'),
    path('revista-libro-conferencia/detalle/<int:pk>/', views.Revista_Libro_Conferencia_Detail.as_view(), name='Revista_Libro_Conferencia_Detail'),
    path('revista-libro-conferencia/eliminar/<int:id>/', views.Revista_Libro_Conferencia_Delete, name='Revista_Libro_Conferencia_Delete'),
    path('revista-libro-conferencia/actualizar/<int:id>/', views.Revista_Libro_Conferencia_Update, name='Revista_Libro_Conferencia_Update'),


# Area
    path('Area_List/', Area_List.as_view(), name='Area_List'),
    path('Area_Create/', Area_Create.as_view(), name='Area_create'),
    path('Area_Update/<int:Area_id>/', Area_Update, name='Area_Update'),
    path('Area_Detail/<int:pk>/', Area_Detail.as_view(), name='Area_Detail'),
    path('Area_Delete/<int:id>/', views.Area_Delete, name='Area_Delete'),

# Departamento
    path('Departamento_List/', Departamento_List.as_view(), name='Departamento_List'),
    path('Departamento_Create/', Departamento_Create.as_view(), name='Departamento_create'),
    path('Departamento_Update/<int:id>/', Departamento_Update, name='Departamento_Update'),
    path('Departamento_Detail/<int:pk>/', Departamento_Detail.as_view(), name='Departamento_Detail'),
    path('Departamento_Delete/<int:id>/', Departamento_Delete, name='Departamento_Delete'),


# Categoría Científica
path('CategoriaCientifica_List/', CategoriaCientificaList.as_view(), name='CategoriaCientificaList'),
path('CategoriaCientifica_Create/', CategoriaCientificaCreate.as_view(), name='CategoriaCientifica_create'),
path('CategoriaCientifica_Update/<int:pk>/', CategoriaCientificaUpdate.as_view(), name='CategoriaCientifica_Update'),
path('CategoriaCientifica_Detail/<int:pk>/', CategoriaCientificaDetail.as_view(), name='CategoriaCientifica_Detail'),
path('CategoriaCientifica_Delete/<int:id>/', CategoriaCientificaDelete, name='CategoriaCientifica_Delete'),

#Colaboradores 
path('Colaboradores_List/', Colaboradores_List.as_view(), name='Colaboradores_List'),
path('Colaboradores_Create/', Colaboradores_Create.as_view(), name='Colaboradores_Create'),
path('Colaboradores_Update/<int:pk>/', Colaboradores_Update.as_view(), name='Colaboradores_Update'),
path('Colaboradores_Detail/<int:pk>/', Colaboradores_Detail.as_view(), name='Colaboradores_Detail'),
path('Colaboradores_Delete/<int:id>/', Colaboradores_Delete, name='Colaboradores_Delete'),

path('tipo_evento/list/', views.TipoEvento_List.as_view(), name='TipoEvento_List'),
path('tipo_evento/create/', views.TipoEvento_Create.as_view(), name='TipoEvento_Create'),
path('tipo_evento/update/<int:pk>/', views.TipoEvento_Update.as_view(), name='TipoEvento_Update'),
path('tipo_evento/detail/<int:pk>/', views.TipoEvento_Detail.as_view(), name='TipoEvento_Detail'),
path('tipo_evento/delete/<int:id>/', views.TipoEvento_Delete, name='TipoEvento_Delete'),

path('tipo_programa/list/', views.TipoPrograma_List.as_view(), name='TipoPrograma_List'),
path('tipo_programa/create/', views.TipoPrograma_Create.as_view(), name='TipoPrograma_Create'),
path('tipo_programa/update/<int:pk>/', views.TipoPrograma_Update.as_view(), name='TipoPrograma_Update'),
path('tipo_programa/detail/<int:pk>/', views.TipoPrograma_Detail.as_view(), name='TipoPrograma_Detail'),
path('tipo_programa/delete/<int:id>/', views.TipoPrograma_Delete, name='TipoPrograma_Delete'),

path('sector_estrategico/list/', views.SectorEstrategico_List.as_view(), name='SectorEstrategico_List'),
path('sector_estrategico/create/', views.SectorEstrategico_Create.as_view(), name='SectorEstrategico_Create'),
path('sector_estrategico/update/<int:pk>/', views.SectorEstrategico_Update.as_view(), name='SectorEstrategico_Update'),
path('sector_estrategico/delete/<int:id>/', views.SectorEstrategico_Delete, name='SectorEstrategico_Delete'),

path('linea_investigacion/list/', views.LineaInvestigacion_List.as_view(), name='LineaInvestigacion_List'),
path('linea_investigacion/create/', views.LineaInvestigacion_Create.as_view(), name='LineaInvestigacion_Create'),
path('linea_investigacion/update/<int:pk>/', views.LineaInvestigacion_Update.as_view(), name='LineaInvestigacion_Update'),
path('linea_investigacion/delete/<int:id>/', views.LineaInvestigacion_Delete, name='LineaInvestigacion_Delete'),

path('tipo_participacion/list/', views.TipoParticipacion_List.as_view(), name='TipoParticipacion_List'),
path('tipo_participacion/create/', views.TipoParticipacion_Create.as_view(), name='TipoParticipacion_Create'),
path('tipo_participacion/update/<int:pk>/', views.TipoParticipacion_Update.as_view(), name='TipoParticipacion_Update'),
path('tipo_participacion/delete/<int:id>/', views.TipoParticipacion_Delete, name='TipoParticipacion_Delete'),

path('tipo_premio/list/', views.TipoPremio_List.as_view(), name='TipoPremio_List'),
path('tipo_premio/create/', views.TipoPremio_Create.as_view(), name='TiposPremio_Create'),
path('tipo_premio/update/<int:pk>/', views.TipoPremio_Update.as_view(), name='TipoPremio_Update'),
path('tipo_premio/detail/<int:pk>/', views.TipoPremio_Detail.as_view(), name='TipoPremio_Detail'),
path('tipo_premio/delete/<int:id>/', views.TipoPremio_Delete, name='TipoPremio_Delete'),
    
path('caracter_premio/list/', views.CaracterPremio_List.as_view(), name='CaracterPremio_List'),
path('caracter_premio/create/', views.CaracterPremio_Create.as_view(), name='CaracteresPremio_Create'),
path('caracter_premio/update/<int:pk>/', views.CaracterPremio_Update.as_view(), name='CaracterPremio_Update'),
path('caracter_premio/detail/<int:pk>/', views.CaracterPremio_Detail.as_view(), name='CaracterPremio_Detail'),
path('caracter_premio/delete/<int:id>/', views.CaracterPremio_Delete, name='CaracterPremio_Delete'),

    # URLs para Modalidad
path('modalidad/list/', views.Modalidad_List.as_view(), name='Modalidad_List'),
path('modalidad/create/', views.Modalidad_Create.as_view(), name='Modalidad_Create'),
path('modalidad/update/<int:pk>/', views.Modalidad_Update.as_view(), name='Modalidad_Update'),
path('modalidad/detail/<int:pk>/', views.Modalidad_Detail.as_view(), name='Modalidad_Detail'),
path('modalidad/delete/<int:id>/', views.Modalidad_Delete, name='Modalidad_Delete'),

# CbASE DE TADOS
path('bases-datos/', views.BasesDatosList.as_view(), name='BasesDatosList'),
path('bases-datos/crear/', views.BasesDatosCreate.as_view(), name='BasesDatos_create'),
path('bases-datos/<int:pk>/', views.BasesDatosDetail.as_view(), name='BasesDatos_detail'),
path('bases-datos/editar/<int:pk>/', views.BasesDatosUpdate.as_view(), name='BasesDatos_Update'),
path('bases-datos/eliminar/<int:id>/', views.BasesDatosDelete, name='BasesDatos_Delete'),

# Categoría Docente
path('CategoriaDocente_List/', CategoriaDocenteList.as_view(), name='CategoriaDocenteList'),
path('CategoriaDocente_Create/', CategoriaDocenteCreate.as_view(), name='CategoriaDocente_create'),
path('CategoriaDocente_Update/<int:pk>/', CategoriaDocenteUpdate.as_view(), name='CategoriaDocente_Update'),
path('CategoriaDocente_Detail/<int:pk>/', CategoriaDocenteDetail.as_view(), name='CategoriaDocente_Detail'),
path('CategoriaDocente_Delete/<int:id>/', CategoriaDocenteDelete, name='CategoriaDocente_Delete'),

# Caracter Evento
path('CarcterEvento_List/', CarcterEvento_List.as_view(), name='CarcterEvento_List'),
path('CarcterEvento_Create/', CarcterEvento_Create.as_view(), name='CarcterEvento_Create'),
path('CarcterEvento_Update/<int:CarcterEvento_id>/', views.CarcterEvento_Update, name='CarcterEvento_Update'),
path('CarcterEvento_Detail/<int:pk>/', CarcterEvento_Detail.as_view(), name='CarcterEvento_Detail'),
path('CarcterEvento_Delete/<int:id>/', CarcterEvento_Delete, name='CarcterEvento_Delete'),

# Cargo
path('Cargo_List/', Cargo_List.as_view(), name='Cargo_List'),
path('Cargo_Create/', Cargo_Create.as_view(), name='Cargo_Create'),
path('Cargo_Update/<int:pk>/', Cargo_Update, name='Cargo_Update'),
path('Cargo_Detail/<int:pk>/', Cargo_Detail.as_view(), name='Cargo_Detail'),
path('Cargo_Delete/<int:id>/', Cargo_Delete, name='Cargo_Delete'),


#..................Usuarios...........................
    
    path('Usuarios/',login_required (views.Usuarios), name="Usuarios"),
    path('EliminarUsuario/<int:id>/',login_required (views.EliminarUsuario), name="EliminarUsuario"),
    path('CambiarRol/<int:id>/',login_required (views.CambiarRol), name="CambiarRol"),
  

   
#..................Perfil Jefe de Area...........................
# Perfil
    path('cambiar-rol-jefe-area/<int:id>/', CambiarRolJefeArea, name='CambiarRolJefeArea'),
    path('Perfil_Create_JefeArea/', Perfil_Create_JefeArea.as_view(), name='Perfil_Create_JefeArea'),
    path('Perfil_Detail_JefeArea/', Perfil_Detail_JefeArea.as_view(), name='Perfil_Detail_JefeArea'),
    path('Perfil_Update_JefeArea/<int:perfil_id>/', Perfil_Update_JefeArea, name='Perfil_Update_JefeArea'),

    path('Articulo_List_JefeArea/', Articulo_List_JefeArea.as_view(), name='Articulo_List_JefeArea'),
    path('Articulo_Detail_JefeArea/<int:pk>/', Articulo_Detail_JefeArea.as_view(), name='Articulo_Detail_JefeArea'),
    path('Articulo_Delete_JefeArea/<int:id>/', Articulo_Delete_JefeArea, name="Articulo_Delete_JefeArea"),
    path('Cambiar_Estado_Articulo/<int:id>/',login_required(Cambiar_Estado_Articulo), name="Cambiar_Estado_Articulo"),
    
    path('Premio_List_JefeArea/', Premio_List_JefeArea.as_view(), name='Premio_List_JefeArea'),
    path('Premio_Detail_JefeArea/<int:pk>/', Premio_Detail_JefeArea.as_view(), name='Premio_Detail_JefeArea'),
    path('Premio_Delete_JefeArea/<int:id>/', Premio_Delete_JefeArea, name="Premio_Delete_JefeArea"),
    path('Cambiar_Estado_Premio/<int:id>/',login_required(Cambiar_Estado_Premio), name="Cambiar_Estado_Premio"),

    path('Proyecto_List_JefeArea/', Proyecto_List_JefeArea.as_view(), name='Proyecto_List_JefeArea'),
    path('Proyecto_Detail_JefeArea/<int:pk>/', Proyecto_Detail_JefeArea.as_view(), name='Proyecto_Detail_JefeArea'),
    path('Proyecto_Delete_JefeArea/<int:id>/', Proyecto_Delete_JefeArea, name="Proyecto_Delete_JefeArea"),
    path('Cambiar_Estado_Proyecto/<int:id>/',login_required(Cambiar_Estado_Proyecto), name="Cambiar_Estado_Proyecto"),
   

    path('Programa_List_JefeArea/', Programa_List_JefeArea.as_view(), name='Programa_List_JefeArea'),
    path('Programa_Detail_JefeArea/<int:pk>/', Programa_Detail_JefeArea.as_view(), name='Programa_Detail_JefeArea'),
    path('Programa_Delete_JefeArea/<int:id>/', Programa_Delete_JefeArea, name="Programa_Delete_JefeArea"),
    path('Cambiar_Estado_Programa/<int:id>/',login_required(Cambiar_Estado_Programa), name="Cambiar_Estado_Programa"),
    

    path('Evento_List_JefeArea/', Evento_List_JefeArea.as_view(), name='Evento_List_JefeArea'),
    path('Evento_Detail_JefeArea/<int:pk>/', Evento_Detail_JefeArea.as_view(), name='Evento_Detail_JefeArea'),
    path('Evento_Delete_JefeArea/<int:id>/', Evento_Delete_JefeArea, name="Evento_Delete_JefeArea"),
    path('Cambiar_Estado_Evento/<int:id>/',login_required(Cambiar_Estado_Evento), name="Cambiar_Estado_Evento"),
  

    path('Informacion_Detail_Investigador_Area/<int:pk>/', Informacion_Detail_Investigador_Area.as_view(), name='Informacion_Detail_Investigador_Area'),
    path('List_Investigador_JefeArea_usuario/', List_Investigador_JefeArea_usuario.as_view(), name='List_Investigador_JefeArea_usuario'),

    path('Curriculo_Investigador_JefeArea/<int:id>/', Curriculo_Investigador_JefeArea.as_view(), name='Curriculo_Investigador_JefeArea'),
    path('Dashboard_JefeArea/', Dashboard_JefeArea.as_view(), name='Dashboard_JefeArea'),

    path('Proyecto_List_Areas/', Proyecto_List_Areas.as_view(), name='Proyecto_List_Areas'),
    path('Articulo_List_Areas/', Articulo_List_Areas.as_view(), name='Articulo_List_Areas'),
    path('Evento_List_Areas/', Evento_List_Areas.as_view(), name='Evento_List_Areas'),
    path('Premio_List_Areas/', Premio_List_Areas.as_view(), name='Premio_List_Areas'),

   
#..................Perfil Jefe de ArDepartamento...........................
# Perfil
    path('Perfil_Create_JefeDepartamento/', Perfil_Create_JefeDepartamento.as_view(), name='Perfil_Create_JefeDepartamento'),
    path('Perfil_Detail_JefeDepartamento/', Perfil_Detail_JefeDepartamento.as_view(), name='Perfil_Detail_JefeDepartamento'),
    path('Perfil_Update_JefeDepartamento/<int:perfil_id>/', Perfil_Update_JefeDepartamento, name='Perfil_Update_JefeDepartamento'),

    path('Articulo_List_Departamento/', Articulo_List_Departamento.as_view(), name='Articulo_List_Departamento'),
    path('Articulo_Delete_JefeDepartamento/<int:id>/', Articulo_Delete_JefeDepartamento, name="Articulo_Delete_JefeDepartamento"),
    path('Articulo_Detail_JefeDepartamento/<int:id>/', Articulo_Detail_JefeDepartamento.as_view(), name="Articulo_Detail_JefeDepartamento"),

    
    path('Premio_List_Departamento/', Premio_List_Departamento.as_view(), name='Premio_List_Departamento'),
    path('Premio_Detail_JefeDepartamento/<int:pk>/', Premio_Detail_JefeDepartamento.as_view(), name='Premio_Detail_JefeDepartamento'),
    path('Premio_Delete_JefeDepartamento/<int:id>/', Premio_Delete_JefeDepartamento, name="Premio_Delete_JefeDepartamento"),
    

    path('Proyecto_List_Departamento/', Proyecto_List_Departamento.as_view(), name='Proyecto_List_Departamento'),
    path('Proyecto_Detail_JefeDepartamento/<int:pk>/', Proyecto_Detail_JefeDepartamento.as_view(), name='Proyecto_Detail_JefeDepartamento'),
    path('Proyecto_Delete_JefeDepartamento/<int:id>/', Proyecto_Delete_JefeDepartamento, name="Proyecto_Delete_JefeDepartamento"),
 

    path('Programa_List_JefeDepartamento/', Programa_List_JefeDepartamento.as_view(), name='Programa_List_JefeDepartamento'),
    path('Programa_Detail_JefeDepartamento/<int:pk>/', Programa_Detail_JefeDepartamento.as_view(), name='Programa_Detail_JefeDepartamento'),
    path('Programa_Delete_JefeDepartamento/<int:id>/', Programa_Delete_JefeDepartamento, name="Programa_Delete_JefeDepartamento"),
    

    path('Evento_List_JefeDepartamento/', Evento_List_JefeDepartamento.as_view(), name='Evento_List_JefeDepartamento'),
    path('Evento_Detail_JefeDepartamento/<int:pk>/', Evento_Detail_JefeDepartamento.as_view(), name='Evento_Detail_JefeDepartamento'),
    path('Evento_Delete_JefeDepartamento/<int:id>/', Evento_Delete_JefeDepartamento, name="Evento_Delete_JefeDepartamento"),
    

    path('Informacion_Detail_Investigador_Departamento/<int:pk>/', Informacion_Detail_Investigador_Departamento.as_view(), name='Informacion_Detail_Investigador_Departamento'),
    path('List_Investigador_JefeDepartamento/', List_Investigador_JefeDepartamento.as_view(), name='List_Investigador_JefeDepartamento'),

    path('Curriculo_Investigador_Departamento/<int:id>/', Curriculo_Investigador_Departamento.as_view(), name='Curriculo_Investigador_Departamento'),
    path('Dashboard_JefeDepartamento/', Dashboard_JefeDepartamento.as_view(), name='Dashboard_JefeDepartamento'),

    path('Proyecto_List_JefeDepartamento/', Proyecto_List_JefeDepartamento.as_view(), name='Proyecto_List_JefeDepartamento'),
    path('Articulo_List_JefeDepartamento/', Articulo_List_JefeDepartamento.as_view(), name='Articulo_List_JefeDepartamento'),
    path('Evento_List_JefeDepartamento/', Evento_List_JefeDepartamento.as_view(), name='Evento_List_JefeDepartamento'),
    path('Premio_List_JefeDepartamento/', Premio_List_JefeDepartamento.as_view(), name='Premio_List_JefeDepartamento'),
   

#VICERRECTOR
    path('cambiar-rol-vicerrector/<int:id>/', CambiarRolVicerrector, name='CambiarRolVicerrector'),
    path('Proyecto_List_Vicerrector/', Proyecto_List_Vicerrector.as_view(), name='Proyecto_List_Vicerrector'),
    path('Articulo_List_Vicerrector/', Articulo_List_Vicerrector.as_view(), name='Articulo_List_Vicerrector'),
    path('Premio_List_Vicerrector/', Premio_List_Vicerrector.as_view(), name='Premio_List_Vicerrector'),
    path('Evento_List_Vicerrector/', Evento_List_Vicerrector.as_view(), name='Evento_List_Vicerrector'),
    path('Programa_List_Vicerrector/', Programa_List_Vicerrector.as_view(), name='Programa_List_Vicerrector'),

    path('List_Investigador_Vicerrector/', List_Investigador_Vicerrector.as_view(), name='List_Investigador_Vicerrector'),
    path('List_Investigador_Vicerrector_Usuario/', List_Investigador_Vicerrector_Usuario.as_view(), name='List_Investigador_Vicerrector_Usuario'),
    
    path('Curriculo_Investigador_Vicerrector/<int:id>/', Curriculo_Investigador_Vicerrector.as_view(), name='Curriculo_Investigador_Vicerrector'),
    path('Informacion_Detail_Investigador_Vicerrector/<int:pk>/', Informacion_Detail_Investigador_Vicerrector.as_view(), name='Informacion_Detail_Investigador_Vicerrector'),

    path('Articulo_Detail_Vicerrector/<int:pk>/', Articulo_Detail_Vicerrector.as_view(), name='Articulo_Detail_Vicerrector'),
    path('Programa_Detail_Vicerrector/<int:pk>/', Programa_Detail_Vicerrector.as_view(), name='Programa_Detail_Vicerrector'),
    path('Proyecto_Detail_Vicerrector/<int:pk>/', Proyecto_Detail_Vicerrector.as_view(), name='Proyecto_Detail_Vicerrector'),
    path('Premio_Detail_Vicerrector/<int:pk>/', Premio_Detail_Vicerrector.as_view(), name='Premio_Detail_Vicerrector'),
    path('Evento_Detail_Vicerrector/<int:pk>/', Evento_Detail_Vicerrector.as_view(), name='Evento_Detail_Vicerrector'),

    path('Dashboard_Vicerrector/', Dashboard_Vicerrector.as_view(), name='Dashboard_Vicerrector'),

    # Perfil
    path('Perfil_Create_Vicerrector/', Perfil_Create_Vicerrector.as_view(), name='Perfil_Create_Vicerrector'),
    path('Perfil_Detail_Vicerrector/', Perfil_Detail_Vicerrector.as_view(), name='Perfil_Detail_Vicerrector'),
    path('Perfil_Update_Vicerrector/<int:perfil_id>/', Perfil_Update_Vicerrector, name='Perfil_Update_Vicerrector'),


#ADMIN
    path('Proyecto_List_Admin/', Proyecto_List_Admin.as_view(), name='Proyecto_List_Admin'),
    path('Articulo_List_Admin/', Articulo_List_Admin.as_view(), name='Articulo_List_Admin'),
    path('Premio_List_Admin/', Premio_List_Admin.as_view(), name='Premio_List_Admin'),
    path('Evento_List_Admin/', Evento_List_Admin.as_view(), name='Evento_List_Admin'),
    path('Programa_List_Admin/', Programa_List_Admin.as_view(), name='Programa_List_Admin'),


    path('Articulo_Detail_Admin/<int:pk>/', Articulo_Detail_Admin.as_view(), name='Articulo_Detail_Admin'),
    path('Programa_Detail_Admin/<int:pk>/', Programa_Detail_Admin.as_view(), name='Programa_Detail_Admin'),
    path('Proyecto_Detail_Admin/<int:pk>/', Proyecto_Detail_Admin.as_view(), name='Proyecto_Detail_Admin'),
    path('Premio_Detail_Admin/<int:pk>/', Premio_Detail_Admin.as_view(), name='Premio_Detail_Admin'),
    path('Evento_Detail_Admin/<int:pk>/', Evento_Detail_Admin.as_view(), name='Evento_Detail_Admin'),
    path('general/editar-nombres-roles/', editar_nombres_roles, name='editar_nombres_roles'),

    path('Dashboard_Admin/', Dashboard_Admin.as_view(), name='Dashboard_Admin'),
    path('api/dashboard/data/', views.api_dashboard_data, name='api_dashboard_data'),


]

urlpatterns = urlpatterns + router.urls

