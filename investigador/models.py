from django.conf import settings
from django.db import models
from plataforma.models import Usuario
from django.core.exceptions import ValidationError
from datetime import date
from plataforma.choices import (
    TIPO, 
    CARACTER, 
    PRESENCIALIDAD, 
    TIPO_PROYECTO_CHOICES, 
    SUBTIPO_PROYECTO_CHOICES,
    APROBACION, 
    SECTOR_ESTRATEGICO_CHOICES,   
    LINEA_INVESTIGACION_CHOICES, 
    ESTADO_PROYECTO_CHOICES, 
    APROBACION,
    CARACTER_EVENTO,
    PAIS,
    CATEGORIAS_CIENTIFICAS,
    CATEGORIAS_DOCENTES,
    ROLES_BASE,
    IDIOMA, GRUPO, PROVINCIAS_CUBA
)
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone


def validate_pag_format(value):
    if value:
        parts = value.split('-')
        if len(parts) != 2:
            raise ValidationError('El formato debe ser "numero-numero" (ej. 12-34)')
        if not all(part.strip().isdigit() for part in parts):
            raise ValidationError('Ambos valores deben ser números')


class Area(models.Model):
    nombre_area = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.nombre_area


class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=50, blank=False, null=False, unique=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.nombre_departamento


class Institucion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name = "Institucion"
        verbose_name_plural = "Instituciones"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    
    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

      
class Categoria_docente(models.Model):
    nombre_categoria_docente = models.CharField(max_length=50, blank = False, null = False, unique = True)

    def __str__(self):
        return self.nombre_categoria_docente


class Categoria_cientifica(models.Model):
    nombre_categoria_cientifica = models.CharField(max_length=50, blank = False, null = False, unique = True)

    def __str__(self):
        return self.nombre_categoria_cientifica


class CarcterEvento(models.Model):
    nombre_caracter_evento = models.CharField(max_length=50, blank = False, null = False, unique = True)

    def __str__(self):
        return self.nombre_caracter_evento


class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=50, blank = False, null = False, unique = True)

    def __str__(self):
        return self.nombre_cargo


class Indexacion(models.Model):
    nombre_base_datos = models.CharField(max_length=50, blank = False, null = False, unique = True)
    grupo = models.CharField(max_length=50, choices=GRUPO, blank=False, null=False, default='Seleccione...')
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.nombre_base_datos


class Colaborador(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    orci = models.CharField(max_length=10, blank=True, null=True)
    google_academico = models.URLField("Google Académico", max_length=200, blank=True)
    rgate = models.URLField("ResearchGate", max_length=200, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    
    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}".strip()


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Tipo de Evento"
        verbose_name_plural = "Tipos de Eventos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Modalidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Modalidad"
        verbose_name_plural = "Modalidades"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


def fecha_no_anterior_a_hoy(value):
    if value < date.today():
        raise ValidationError("La fecha no puede ser anterior a hoy.")

    
class Proyecto(models.Model):
    marcador = 'Proyecto'
    codigo_proyecto = models.CharField(max_length=36, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_proyecto = models.CharField(max_length=255, blank = False, null = False)
    jefe_proyecto = models.CharField(max_length = 150, blank=False, null=False)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_proyecto = models.CharField(max_length=50, choices=TIPO_PROYECTO_CHOICES, blank = False, null = False)
    subtipo_proyecto = models.CharField(max_length = 50, choices=SUBTIPO_PROYECTO_CHOICES, blank=True, null=True)
    entidades_participantes = models.TextField(max_length = 150, blank = False, null = False)
    sector_estrategico = models.CharField(max_length=100, choices=SECTOR_ESTRATEGICO_CHOICES, blank = False, null = False)
    linea_investigacion = models.CharField(max_length=100, choices=LINEA_INVESTIGACION_CHOICES,blank = False, null = False)
    fecha_inicio = models.DateField(validators=[fecha_no_anterior_a_hoy], blank=False, null=False)
    fecha_cierre = models.DateField(validators=[fecha_no_anterior_a_hoy], blank=False, null=False)
    estado_proyecto = models.CharField(max_length=10, choices=ESTADO_PROYECTO_CHOICES, blank = False, null = False)
    cantidad_profesores_trabajadores_uho = models.CharField(max_length = 11, blank=False, null=False)
    cantidad_estudiantes_contratados = models.CharField(max_length = 11, blank=False, null=False)
    cantidad_participantes_otras_entidades = models.CharField(max_length = 11, blank=False, null=False)
    cantidad_profesores_colaboradores_uho = models.CharField(max_length = 11, blank=False, null=False)
    cantidad_estudiantes_grupos_cientificos = models.CharField(max_length = 11, blank=False, null=False)
    cantidad_colaboradores_otras_entidades = models.CharField(max_length = 11, blank=False, null=False)
    cantidad_estudiantes_segundo_adelante = models.CharField(max_length = 11, blank=False, null=False)
    cantidad_cuadros_uho = models.CharField(max_length = 11, blank=False, null=False)
    presupuesto_planificado = models.CharField(max_length = 11, blank=False, null=False)
    presupuesto_ejecutado_primer_semestre = models.CharField(max_length = 11, blank=False, null=False)
    presupuesto_ejecutado_segundo_semestre = models.CharField(max_length = 11, blank=False, null=False)
    aprobacion = models.CharField(max_length=10, blank=False, null=False, choices=APROBACION, default= 'Pendiente')
    fecha_create = models.DateField(blank=False, null=False, auto_now=True)

    def save(self, *args, **kwargs):
            if self.pk is not None:  
                previous = Proyecto.objects.get(pk=self.pk)
                if previous.aprobacion == 'No Valido':
                    self.aprobacion = 'Pendiente'
            super(Proyecto, self).save(*args, **kwargs)
    def __str__(self):
        return self.nombre_proyecto


class TipoPrograma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Programa"
        verbose_name_plural = "Tipos de Programa"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class SectorEstrategico(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Sector Estratégico"
        verbose_name_plural = "Sectores Estratégicos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class LineaInvestigacion(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo = models.CharField(max_length=15, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Línea de Investigación"
        verbose_name_plural = "Líneas de Investigación"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class EntidadParticipante(models.Model):
    TIPOS_ENTIDAD = [
        ('Universidad', 'Universidad'),
        ('Instituto', 'Instituto de Investigación'),
        ('Centro', 'Centro de Investigación'),
        ('Empresa', 'Empresa'),
        ('Ministerio', 'Ministerio'),
        ('Hospital', 'Hospital/Centro de Salud'),
        ('ONG', 'Organización No Gubernamental'),
        ('Internacional', 'Organización Internacional'),
        ('Otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=250, unique=True)
    sigla = models.CharField(max_length=20, blank=True, null=True)
    tipo_entidad = models.CharField(max_length=20, choices=TIPOS_ENTIDAD, default='Otro')
    pais = models.CharField(max_length=100, default='Cuba')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Entidad Participante"
        verbose_name_plural = "Entidades Participantes"
        ordering = ['nombre']
    
    def __str__(self):
        if self.sigla:
            return f"{self.nombre} ({self.sigla})"
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Normalizar nombre
        self.nombre = self.nombre.strip().title()
        if self.sigla:
            self.sigla = self.sigla.strip().upper()
        super().save(*args, **kwargs)


class TipoParticipacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Participación"
        verbose_name_plural = "Tipos de Participación"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Programa(models.Model):
    # Campos básicos del programa
    nombre_programa = models.CharField(max_length=300, verbose_name="Nombre del Programa")
    codigo_programa = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Código",
        validators=[RegexValidator(
            regex=r'^[A-Z0-9\-]+$',
            message='El código debe contener solo letras mayúsculas, números y guiones'
        )]
    )
    tipo_programa = models.ForeignKey(
        TipoPrograma, 
        on_delete=models.PROTECT,
        verbose_name="Tipo de Programa"
    )
    
    # Organización y ejecución
    organismo = models.CharField(max_length=200, verbose_name="Organismo")
    entidad_ejecutora = models.CharField(max_length=200, verbose_name="Entidad Ejecutora")
    jefe_programa = models.CharField(max_length=200, verbose_name="Jefe del Programa")
    
    # Fechas
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Finalización")
    
    # Clasificación
    sector_estrategico = models.ForeignKey(
        SectorEstrategico,
        on_delete=models.PROTECT,
        verbose_name="Sector Estratégico"
    )
    linea_investigacion = models.ForeignKey(
        LineaInvestigacion,
        on_delete=models.PROTECT,
        verbose_name="Línea de Investigación de la UHO"
    )
    
    # Relaciones
    entidades_participantes = models.ManyToManyField(
        EntidadParticipante,
        through='ProgramaEntidad',
        blank=True,
        verbose_name="Entidades Participantes"
    )
    
    # Metadatos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Creado por")
    fecha_create = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    aprobacion = models.CharField(max_length=10, blank=False, null=False, choices=APROBACION, default= 'Pendiente')
    area = models.ForeignKey('investigador.Area', on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey('investigador.Departamento', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
        ordering = ['-fecha_create']
    
    def __str__(self):
        return f"{self.codigo_programa} - {self.nombre_programa}"
    
    @property
    def duracion_meses(self):
        """Calcula la duración del programa en meses"""
        if self.fecha_inicio and self.fecha_fin:
            delta = self.fecha_fin - self.fecha_inicio
            return round(delta.days / 30.44)  # Promedio de días por mes
        return 0


class ProgramaEntidad(models.Model):
    """Modelo intermedio para la relación Programa-EntidadParticipante"""
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    entidad = models.ForeignKey(EntidadParticipante, on_delete=models.CASCADE)
    fecha_incorporacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['programa', 'entidad']
        verbose_name = "Programa-Entidad"
        verbose_name_plural = "Programa-Entidades"


class ParticipacionPrograma(models.Model):
    """Participantes de la UHO en el programa"""
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name='participaciones')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_participacion = models.ForeignKey(TipoParticipacion, on_delete=models.PROTECT,verbose_name="Tipo de Participación")
    fecha_incorporacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['programa', 'usuario']
        verbose_name = "Participación en Programa"
        verbose_name_plural = "Participaciones en Programas"
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.programa.codigo_programa}"

    
class EventoBase(models.Model):
    titulo = models.CharField(max_length=200, default=None, null=False, blank=False, verbose_name="Título del evento")
    tipo =  models.ForeignKey(TipoEvento, on_delete=models.SET_NULL, null=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Institución responsable")
    pais = models.CharField(max_length=100, verbose_name="País", null=False, blank=False)
    provincia = models.CharField(max_length=3, choices=PROVINCIAS_CUBA, blank=True, null=True, verbose_name="Provincia")
    
    class Meta:
        verbose_name = "Evento Base"
        verbose_name_plural = "Eventos Base"
        ordering = ['titulo']

    @property
    def mes_ano(self):
        """Devuelve el mes y año formateados"""
        if self.fecha:
            return self.fecha.strftime("%B %Y")  # Ejemplo: "Enero 2023"
        return ""
    
    def __str__(self):
        return self.titulo


class Evento(models.Model):
    marcador = 'Evento'
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_creados')
    evento_base = models.ForeignKey('EventoBase', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Evento Base")
    titulo = models.CharField(max_length=200)
    tipo =  models.ForeignKey(TipoEvento, on_delete=models.SET_NULL, null=True)
    modalidad =  models.ForeignKey(Modalidad, on_delete=models.SET_NULL, null=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Institución responsable")
    isbn = models.CharField(max_length=10, blank=True, null=True)
    fecha_create = models.DateField(blank=False, null=False)
    pais = models.CharField(max_length=100, blank=False, null=False, verbose_name="País")
    provincia = models.CharField(max_length=3, choices=PROVINCIAS_CUBA, blank=True, null=True, verbose_name="Provincia")
    nombre_ponencia = models.CharField(max_length=200, blank=False, null=False)
    url = models.URLField(max_length=200, blank=True, null=True)
    certificado = models.FileField(upload_to='Eventos/', blank=True, null=True)
    aprobacion = models.CharField(max_length=50, blank=False, null=False, choices=APROBACION, default='Pendiente')
    area = models.ForeignKey('investigador.Area', on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey('investigador.Departamento', on_delete=models.SET_NULL, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    
    def autores(self):
        return EventoAutor.objects.filter(evento=self)
    
    def save(self, *args, **kwargs):
        # Asignar automáticamente área y departamento del usuario creador
        if not self.area_id and self.usuario_id:
            self.area = self.usuario.area
        
        if not self.departamento_id and self.usuario_id:
            self.departamento = self.usuario.departamento
        
     
        if self.pk is not None:  
            previous = Evento.objects.get(pk=self.pk)
            if previous.aprobacion == 'No Valido':
                self.aprobacion = 'Pendiente'
        
        super().save(*args, **kwargs)
        
    @property
    def mes_ano(self):
        if self.fecha_create:
            return self.fecha_create.strftime("%B %Y")
        return ""
   
    def __str__(self):
        return self.titulo


class EventoAutor(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="eventos_set")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('evento', 'usuario', 'colaborador')  # Evita duplicados

    def nombre_completo(self):
        if self.usuario:
            full_name = self.usuario.get_full_name()
            return full_name if full_name.strip() else self.usuario.username
        if self.colaborador:
            return f"{self.colaborador.nombre} {self.colaborador.apellidos}".strip()
        return "Desconocido"

    
    def __str__(self):
        if self.usuario:
            return self.usuario.get_full_name() or self.usuario.username
        elif self.colaborador:
            return f"{self.colaborador.nombre} {self.colaborador.apellidos}"
        return "Autor sin nombre"


class TipoPremio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Tipo de Premio")
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, verbose_name="Institución que lo otorga")
    
    class Meta:
        verbose_name = "Tipo de Premio"
        verbose_name_plural = "Tipos de Premios"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    
class CaracterPremio(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Carácter de Premio")
    
    class Meta:
        verbose_name = "Carácter de Premio"
        verbose_name_plural = "Carácteres de Premios"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

    
class Premio(models.Model):
    marcador = 'Premio'
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='premios_creados')
    tipo = models.ForeignKey('TipoPremio', on_delete=models.CASCADE, blank=False, null=False)
    caracter = models.ForeignKey('CaracterPremio', on_delete=models.CASCADE, blank=False, null=False)
    titulo = models.CharField(max_length=200, null=True, blank=True)
    fecha_create = models.DateField(blank=False, null=False)
    diploma = models.FileField(upload_to='Premios/', blank=True, null=True)
    area = models.ForeignKey('investigador.Area', on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey('investigador.Departamento', on_delete=models.SET_NULL, null=True, blank=True)
    aprobacion = models.CharField(max_length=50, choices=APROBACION, default='Pendiente')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:  
            previous = Premio.objects.get(pk=self.pk)
            if previous.aprobacion == 'No Valido':
                self.aprobacion = 'Pendiente'
        super(Premio, self).save(*args, **kwargs)   
        
    def premiados(self):
        return PremioPremiado.objects.filter(premio=self)

    def __str__(self):
        return self.titulo or f"Premio #{self.pk or 'sin ID'}"


class PremioPremiado(models.Model):
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE, related_name="premiados_set")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('premio', 'usuario', 'colaborador')  # Evita duplicados

    def nombre_completo(self):
        if self.usuario:
            return self.usuario.get_full_name()
        if self.colaborador:
            return f"{self.colaborador.nombre} {self.colaborador.apellidos}"
        return ''
    
    def __str__(self):
        if self.usuario:
            return self.usuario.get_full_name() or self.usuario.username
        elif self.colaborador:
            return f"{self.colaborador.nombre} {self.colaborador.apellidos}"
        return "Premiado sin nombre"

          
class Perfil(models.Model):
    marcador = 'Perfil'
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length = 150, blank=False, null=False)
    apellidos = models.CharField(max_length = 150, blank=False, null=False)
    ci = models.CharField(max_length = 11, blank=False, null=False)
    email = models.EmailField(max_length = 50, blank=False, null=False)
    telefono = models.CharField(max_length = 8, blank=False, null=False)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    categoria_cientifica = models.ForeignKey(Categoria_cientifica, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    categoria_docente = models.ForeignKey(Categoria_docente, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    orci = models.CharField(max_length=10, blank=True)
    google_academico = models.URLField((""), max_length=200, blank=True)
    rgate = models.URLField((""), max_length=200, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    proyecto = models.ManyToManyField(Proyecto, blank=True, related_name='proyectos_a_los_que_pertenece')
    
    def save(self, *args, **kwargs):
        # Actualizar área y departamento desde el usuario asociado si existe
        if self.usuario:
            # Actualizar área si el usuario tiene una asignada
            if self.usuario.area:
                self.area = self.usuario.area
            
            # Actualizar departamento si el usuario tiene uno asignado
            if self.usuario.departamento:
                self.departamento = self.usuario.departamento
        
        # Llamar al método save original
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre


class Revista_Libro_Conferencia(models.Model):
    titulo = models.CharField(max_length=200, blank=False, null=False)
    editorial = models.CharField(max_length=200, blank=False, null=False)
    issn = models.CharField(max_length=9, blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True, choices=PAIS)
    idioma = models.CharField(max_length=50, blank=True, null=True, choices=IDIOMA)
    url = models.URLField(max_length=200, blank=True, null=True)
    index = models.ForeignKey(Indexacion, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    cita = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True,  related_name='revistas_creados')
    class Meta:
        verbose_name = "Revista/Libro/Conferencia"
        verbose_name_plural = "Revistas/Libros/Conferencias"
    
    def __str__(self):
        return f"{self.titulo} ({self.editorial})"


class Articulo(models.Model):
    marcador = 'Articulo'
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='articulos_creados')
    titulo = models.CharField(max_length=200, blank=False, null=False)
    doi = models.CharField(max_length=50, blank=False, null=False) 
    issn_isbn = models.CharField(max_length=9, blank=False, null=False)
    fecha_create = models.DateField(blank=False, null=False)
    idioma = models.CharField(max_length=50, blank=True, null=True, choices=IDIOMA, default='Seleccione...')
    revista = models.ForeignKey(Revista_Libro_Conferencia, on_delete=models.CASCADE, blank=True, null=True)
    editorial = models.CharField(max_length=200, blank=False, null=False)
    volumen = models.CharField(max_length=10, blank=False, null=False)
    numero = models.CharField(max_length=10, blank=True, null=True, default=0)
    pag = models.CharField(max_length=20,blank=True,null=True,validators=[validate_pag_format], help_text='Formato: numero-numero (ej. 12-34)')
    indexacion = models.ForeignKey(Indexacion, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    url = models.URLField(max_length=200, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=False, null=False, verbose_name="País")
    archivo = models.FileField(upload_to='Articulos/', blank=True, null=True)
    forma_citar = models.CharField(max_length=400, blank=True, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    departamento = models.ForeignKey('Departamento', on_delete=models.SET_NULL, null=True, blank=True)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True)
    aprobacion = models.CharField(max_length=50, blank=True, null=True, choices=APROBACION, default='Pendiente')
    
    def autores(self):
        return ArticuloAutor.objects.filter(articulo=self)
    
    def save(self, *args, **kwargs):
        if not self.area_id and self.usuario_id:
            self.area = self.usuario.area
        
        if not self.departamento_id and self.usuario_id:
            self.departamento = self.usuario.departamento
        
        if self.pk is not None:  
            previous = Articulo.objects.get(pk=self.pk)
            if previous.aprobacion == 'No Valido':
                self.aprobacion = 'Pendiente'
        
        super().save(*args, **kwargs)
  

    def __str__(self):
        return self.titulo 


class ArticuloAutor(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name="articulos_set")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('articulo', 'usuario', 'colaborador') 

    def nombre_completo(self):
        if self.usuario:
            full_name = self.usuario.get_full_name()
            return full_name if full_name.strip() else self.usuario.username
        if self.colaborador:
            return f"{self.colaborador.nombre} {self.colaborador.apellidos}".strip()
        return "Desconocido"

    
    def __str__(self):
        if self.usuario:
            return self.usuario.get_full_name() or self.usuario.username
        elif self.colaborador:
            return f"{self.colaborador.nombre} {self.colaborador.apellidos}"
        return "Autor sin nombre"


class Notificacion(models.Model):
    usuario = models.ForeignKey('plataforma.Usuario', on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo_contenido = models.CharField(max_length=50)  # 'Articulo', 'Evento', 'Premio', etc.
    id_contenido = models.PositiveIntegerField()  # ID del objeto relacionado
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    def marcar_como_leida(self):
        self.leida = True
        self.save()        