from django.core.cache import cache
from django.db.utils import OperationalError, ProgrammingError

ROLES_BASE = (
    ('Administrador', 'Administrador'),
    ('Vicerrector', 'Vicerrector'),
    ('Jefe_departamento', 'Jefe de departamento'),
    ('Jefe_area', 'Jefe de area'),
    ('Investigador', 'Investigador'),
)

def obtener_roles_personalizados():

    try:
        from plataforma.models import NombreRol 
        
        cached_roles = cache.get('roles_personalizados_cache')
        if cached_roles:
            return cached_roles
        
        try:
            nombres_personalizados = {
                rol.codigo: rol.nombre_personalizado 
                for rol in NombreRol.objects.all()
            }
            
            roles_actualizados = [
                (codigo, nombres_personalizados.get(codigo, nombre_default))
                for codigo, nombre_default in ROLES_BASE
            ]
            
            cache.set('roles_personalizados_cache', roles_actualizados, timeout=3600)
            return roles_actualizados
        except (OperationalError, ProgrammingError):
            
            return ROLES_BASE
    except ImportError:

        return ROLES_BASE

ROLES_USUARIO = obtener_roles_personalizados()


CATEGORIAS_CIENTIFICAS = (
    ('Investigador Agregado', 'Investigador Agregado'),
    ('Investigador Auxiliar', 'Investigador Auxiliar'),
    ('Investigador Titular', 'Investigador Titular'),
)

CATEGORIAS_DOCENTES = (
    ('Estudiante', 'Estudiante'),
    ('Licenciado', 'Licenciado'),
    ('Maestria', 'Maestria'),
    ('Doctorado', 'Doctorado'),
)


CARACTER = [
        ('Congreso','Congreso'),
        ('Jornada','Jornada'),
        ('Foro','Foro'),
        ('Conferencia','Conferencia'),
        ('Panel','Panel'),
        ('Simposio','Simposio'),
        ('Mesa Redonda','Mesa Redonda'),
        ('Taller','Taller'),
        ('Seminario','Seminario'),
        ('Convencion','Convencion'),
        ('Encuentro','Encuentro'),
]

DEPARTAMENTOS_CHOICES = [
        ('CECID', 'CECID'),
        ('CEGEDEL', 'CEGEDEL'),
        ('CENFOLAB', 'CENFOLAB'),
        ('AFITCOMB', 'AFITCOMB'),
        ('CEGO', 'CEGO'),
        ('CECE', 'CECE'),
        ('CEAR', 'CEAR'),
        ('CADCAN', 'CADCAN'),
        # Introducir otros departamentos si es necesario
    ]

ESTADO_PROYECTO_CHOICES = [
        ('Normal', 'Normal'),
        ('Atrasado', 'Atrasado'),
        ('Terminado', 'Terminado'),
        ('Cancelado', 'Cancelado'),
        ('Prórroga', 'Prórroga'),
    ]

TIPO_PROYECTO_CHOICES = [
        ('PAPN', 'Proyectos Asociados a Programas Nacionales'),
        ('PAPS', 'Proyectos Asociados a Programas Sectoriales'),
        ('PAPT', 'Proyectos Asociados a Programas Territoriales'),
        ('PNAP', 'Proyectos No Asociados a Programas'),
    ]

SUBTIPO_PROYECTO_CHOICES = [
        ('PI', 'Proyectos Institucionales'),
        ('PE', 'Proyectos Empresariales'),
        ('PNE', 'Proyectos con Entidades No Empresariales y de la Administración Pública'),
        ('PDL', 'Proyectos de Desarrollo Local'),
        ('PRCI', 'Proyectos en Relación con la Colaboración Internacional'),
    ]

SECTOR_ESTRATEGICO_CHOICES = [
        ('Sector productor de alimentos', 'Sector productor de alimentos'),
        ('Industria Ligera', 'Industria Ligera'),
        ('Servicios técnicos profesionales', 'Servicios técnicos profesionales'),
        ('Industria', 'Industria'),
        ('Agroindustria azucarera y sus derivados', 'Agroindustria azucarera y sus derivados'),
        ('Industria farmacéutica, biotecnológica y', 'Industria farmacéutica, biotecnológica y'),
        ('Turismo', 'Turismo'),
        ('Logística integrada de redes e instalaciones', 'Logística integrada de redes e instalaciones'),
        ('Logística integrada de transporte', 'Logística integrada de transporte'),
        ('Telecomunicaciones', 'Telecomunicaciones'),
        ('Electroenergético', 'Electroenergético'),
        ('Construcciones', 'Construcciones'),
        # Add other sectors as needed
    ]

LINEA_INVESTIGACION_CHOICES = [
        ('Línea 1', 'Línea de Investigación 1'),
        ('Línea 2', 'Línea de Investigación 2'),
        ('Línea 3', 'Línea de Investigación 3'),
        # Modificar despues
    ]
    
PRESENCIALIDAD = [
	('Presencial','Presencial'),
	('Virtual','Virtual'),
	('Mixto','Mixto'),
]





APROBACION = [
    ('Pendiente','Pendiente'),
    ('No Valido','No Valido'),
	('Aprobado','Aprobado'),
]

TIPO = [
    ('Regional','Regional'),
	('Nacional','Nacional'),
	('Internacional','Internacional'),
    ]

CARACTER_EVENTO = [
    ('Ninguno','Ninguno'),
	('Forum Ciencia Tecnica}','Forum Ciencia Tecnica'),
	('Forum Nacionales Estudiantiles','Forum Nacionales Estudiantiles'),
    ('Jornadas Cientificas Estudiantiles','Jornadas Cientificas Estudiantiles'),
	
]

PAIS = [
	('Cuba','Cuba'),
	('Otro','Otro')
]

IDIOMA = [
	('Espanol','Espanol'),
    ('Ingles','Ingles'),
	('Portugues','Portugues'),
    ('Otro','Otro')
]

GRUPO = [
    ('Grupo 1','Grupo 1'),
	('Grupo 2','Grupo 2'),
	('Grupo 3','Grupo 3'),
    ('Grupo 4','Grupo 4'),
	
]

PROVINCIAS_CUBA = [
    ('PRI', 'Pinar del Río'),
    ('ART', 'Artemisa'),
    ('HAB', 'La Habana'),
    ('MAY', 'Mayabeque'),
    ('MTZ', 'Matanzas'),
    ('CFG', 'Cienfuegos'),
    ('VCL', 'Villa Clara'),
    ('SSP', 'Sancti Spíritus'),
    ('CAV', 'Ciego de Ávila'),
    ('CMG', 'Camagüey'),
    ('LTU', 'Las Tunas'),
    ('HOL', 'Holguín'),
    ('GRA', 'Granma'),
    ('SCU', 'Santiago de Cuba'),
    ('GTM', 'Guantánamo'),
    ('IJV', 'Isla de la Juventud'),
]

