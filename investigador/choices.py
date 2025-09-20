
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
        # Add other departments and centers as needed
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
        ('Industria farmacéutica, biotecnológica', 'Industria farmacéutica, biotecnológica'),
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
        # Add other lines as needed
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
    ('Facultad','Facultad'),
    ('Institutional','Institutional'),
    ('Municipal','Municipal'),
    ('Regional','Regional'),
    ('Provincial','Provincial'),
	('Nacional','Nacional'),
	('Internacional','Internacional'),
    ]

CARACTER_EVENTO = [
    ('Ninguno','Ninguno'),
	('Forum Ciencia Tecnica}','Forum Ciencia Tecnica'),
	('Forum Nacionales Estudiantiles','Forum Nacionales Estudiantiles'),
    ('Jornadas Cientificas Estudiantiles','Jornadas Cientificas Estudiantiles'),
	
]

GRUPO = [
    ('Grupo 1','Grupo 1'),
	('Grupo 2','Grupo 2'),
	('Grupo 3','Grupo 3'),
    ('Grupo 4','Grupo 4'),
	
]
PAIS = [
	('Cuba','Cuba'),
	('Otro','Otro')
]

PROVINCIAS_CUBA = [
    ('PRI', 'Pinar del Río'),
    ('ART', 'Artemisa'),
    ('HAB', 'La Habana'),
    ('MAY', 'Mayabeque'),
    ('MTZ', 'Matanzas'),
    ('VCL', 'Villa Clara'),
    ('CFG', 'Cienfuegos'),
    ('SSP', 'Sancti Spíritus'),
    ('CAV', 'Ciego de Ávila'),
    ('CAM', 'Camagüey'),
    ('LTU', 'Las Tunas'),
    ('HOL', 'Holguín'),
    ('GRA', 'Granma'),
    ('SCU', 'Santiago de Cuba'),
    ('GTM', 'Guantánamo'),
    ('IJV', 'Isla de la Juventud'),
]


