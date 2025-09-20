from django.contrib import admin
from .models import (
	Evento,Perfil,Articulo,Proyecto,Premio,Programa, Area, Departamento, Categoria_docente, Categoria_cientifica, CarcterEvento, PremioPremiado,
	Cargo, Revista_Libro_Conferencia, Colaborador, EventoBase, TipoEvento, Modalidad, Indexacion, ParticipacionPrograma, Institucion, EventoAutor,
	TipoParticipacion, EntidadParticipante, LineaInvestigacion, ProgramaEntidad, TipoPrograma, SectorEstrategico, TipoPremio, CaracterPremio
)
# Register your models here.

admin.site.register(Evento)
admin.site.register(Perfil)
admin.site.register(PremioPremiado)
admin.site.register(Institucion)
admin.site.register(Premio)
admin.site.register(Articulo)
admin.site.register(Proyecto)
admin.site.register(Programa)
admin.site.register(Area)
admin.site.register(Departamento)
admin.site.register(Categoria_docente)
admin.site.register(Categoria_cientifica)
admin.site.register(CarcterEvento)
admin.site.register(Cargo)
admin.site.register(Revista_Libro_Conferencia)
admin.site.register(Colaborador)
admin.site.register(EventoBase)
admin.site.register(Modalidad)
admin.site.register(TipoEvento)
admin.site.register(Indexacion)
admin.site.register(ParticipacionPrograma)
admin.site.register(TipoParticipacion)
admin.site.register(EntidadParticipante)
admin.site.register(LineaInvestigacion)
admin.site.register(ProgramaEntidad)
admin.site.register(TipoPrograma)
admin.site.register(SectorEstrategico)
admin.site.register(TipoPremio)
admin.site.register(CaracterPremio)
admin.site.register(EventoAutor)

