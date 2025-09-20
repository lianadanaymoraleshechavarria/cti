from .models import (
                     Evento, Proyecto, Programa, Premio, Perfil, Articulo, TipoPremio, CaracterPremio,
                     Area, Departamento, Categoria_docente, Categoria_cientifica, Institucion,
                     CarcterEvento, Cargo, Revista_Libro_Conferencia, Colaborador,
                     Indexacion, TipoEvento, Modalidad, EventoBase, SectorEstrategico, 
                     LineaInvestigacion, EntidadParticipante, TipoParticipacion, TipoPrograma
    )
from django import forms
from dal import autocomplete
from plataforma.models import Usuario
import json


class Revista_Libro_Conferencia_Form(forms.ModelForm):
    
    class Meta:
        model = Revista_Libro_Conferencia
        fields = ('titulo', 'editorial', 'issn', 'isbn', 'pais', 'idioma', 'index', 'cita', 'url') 

        widgets = {
            'titulo': forms.TextInput(attrs={'type':'text','name':'titulo','id':'titulo','class':'form-control', 'placeholder':'Introduzca el Título'}),
            'editorial': forms.TextInput(attrs={'type':'text','name':'editorial','id':'editorial','class':'form-control', 'placeholder': 'Coloque el nombre de la editorial'}),
            'issn': forms.NumberInput(attrs={'type':'text','name':'issn','id':'issn','class':'form-control','placeholder':'Introduzca el ISSN'}),
            'isbn': forms.TextInput(attrs={'type':'text','name':'isbn','id':'isbn','class':'form-control','placeholder':'Introduzca el ISBN'}),
            'idioma': forms.Select(attrs={'class': 'form-control','placeholder':'Introduzca el Idioma en que se ecnuentra'}),
            'pais': forms.Select(attrs={'class': 'form-control','placeholder':'Introduzca el pais de origen'}),
            'index': forms.Select(attrs={'class': 'form-control','placeholder':'Index'}),
            'cita': forms.Select(attrs={'class': 'form-control','placeholder':'Forma de citar'}),
            'url': forms.URLInput(attrs={'name':'url','id':'url','class':'form-control', 'placeholder':'Introduzca la url'}),
        }

        help_texts = {
            'titulo': 'Ingrese el título o nombre completo.',
            'editorial': 'Proporcione el nombre de la editorial responsable.',
            'issn': 'Introduzca el número ISSN válido, si aplica.',
            'isbn': 'Introduzca el número ISBN válido, si aplica.',
            'pais': 'Seleccione el país de publicación.',
            'idioma': 'Seleccione el idioma principal de la obra.',
            'index': 'Seleccione el idioma principal de la obra.',
            'cita': 'Seleccione el idioma principal de la obra.',
        }


class Area_Form(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre_area']
        widgets = {
            'nombre_area': forms.TextInput(attrs={'placeholder': 'Nombre del Área'}),
        }
        help_texts = {
            'nombre_area': 'Ingrese el nombre del área de estudio o trabajo.',
        }


class Departamento_Form(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nombre_departamento', 'area']
        widgets = {
            'nombre_departamento': forms.TextInput(attrs={'placeholder': 'Nombre del Departamento'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'nombre_departamento': 'Ingrese el nombre del departamento.',
            'area': 'Seleccione el área correspondiente al departamento.',
        }


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control required-field'}),
        }
        

class CategoriaDocenteForm(forms.ModelForm):
    class Meta:
        model = Categoria_docente
        fields = ['nombre_categoria_docente']
        widgets = {
            'nombre_categoria_docente': forms.TextInput(attrs={'placeholder': 'Nombre del la caregoria'}),
        }
        help_texts = {
            'nombre_categoria_docente': 'Ingrese el nombre de la categoría docente.',
        }


class CategoriaCientificaForm(forms.ModelForm):
    class Meta:
        model = Categoria_cientifica
        fields = ['nombre_categoria_cientifica']
        widgets = {
            'nombre_categoria_cientifica': forms.TextInput(attrs={'placeholder': 'Nombre del Departamento'}),
        }
        help_texts = {
            'nombre_categoria_cientifica': 'Ingrese el nombre de la categoría científica.',
        }


class CarcterEvento_Form(forms.ModelForm):
    class Meta:
        model = CarcterEvento
        fields = ['nombre_caracter_evento']
        widgets = {
            'nombre_caracter_evento': forms.TextInput(attrs={'placeholder': 'Nombre de caracter'}),
        }
        help_texts = {
            'nombre_caracter_evento': 'Ingrese el nombre que define el carácter del evento.',
        }


class Cargo_Form(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre_cargo']
        widgets = {
            'nombre_cargo': forms.TextInput(attrs={'placeholder': 'Nombre del cargo'}),
        }
        help_texts = {
            'nombre_cargo': 'Ingrese el nombre del cargo correspondiente.',
        }


class Colaborador_Form(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nombre', 'apellidos', 'orci', 'google_academico', 'rgate']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: María', 'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Ej: García López', 'class': 'form-control'}),
            'orci': forms.TextInput(attrs={'placeholder': 'Ej: 0000-0001-2345-6789', 'class': 'form-control'}),
            'google_academico': forms.URLInput(attrs={
                'placeholder': 'https://scholar.google.com/citations?user=ID', 'class': 'form-control'
            }),
            'rgate': forms.URLInput(attrs={
                'placeholder': 'https://www.researchgate.net/profile/Nombre_Apellido', 'class': 'form-control'
            })
        }
        help_texts = {
            'orci': 'Identificador ORCID (opcional)',
            'google_academico': 'URL de tu perfil de Google Académico',
            'rgate': 'URL de tu perfil de ResearchGate'
        }
        labels = {
            'google_academico': 'Google Académico',
            'rgate': 'ResearchGate'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.usuario = self.user
        if commit:
            instance.save()
        return instance


class EventoBaseForm(forms.ModelForm):
    class Meta:
        model = EventoBase
        fields = ['titulo', 'tipo', 'institucion', 'pais', 'provincia']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del evento base'}),
            'tipo': forms.Select(attrs={'type':'text','name':'tipo','id':'ortipoganismo','class':'form-control', 'placeholder':'Seleccione el tipo de evento'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institución responsable'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}),
            'provincia': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Provincia (solo si es Cuba)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(EventoBaseForm, self).__init__(*args, **kwargs)
        # Filtrar provincias solo de Cuba (si estás usando un modelo Provincia)
        if hasattr(self, 'fields') and 'provincia' in self.fields:
            self.fields['provincia'].required = False
        
        # Configurar formatos de fecha aceptados
        self.fields['fecha'].input_formats = ['%Y-%m', '%m/%Y', '%Y/%m']
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            # Forzar el día a 1 para consistencia en la base de datos
            return fecha.replace(day=1)
        return fecha
    

class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ModalidadForm(forms.ModelForm):
    class Meta:
        model = Modalidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AnyValueMultipleChoiceField(forms.MultipleChoiceField):
    def validate(self, value):
        # saltar validación de choices
        return

class Evento_Form(forms.ModelForm):
    evento_base = forms.ModelChoiceField(
        queryset=EventoBase.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'display:none;'}),
        label="Evento Base"
    )
    
    autores = AnyValueMultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'display:none;'})
    )
    
    class Meta:
        model = Evento
        fields = [
            'evento_base',
            'titulo',
            'fecha_create',
            'certificado',
            'tipo',
            'modalidad',
            'isbn',   
            'area',
            'departamento',
            'institucion',
            'pais',
            'provincia',
            'nombre_ponencia',
            'url',
            'proyecto'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'type':'text','name':'titulo','id':'id_titulo','class':'form-control', 'style':'position:absolute; left:-9999px;', 'placeholder':'Introduzca el Título'}),
            'fecha_create': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'id': 'fecha_create', 'class': 'form-control'}),
            'certificado': forms.FileInput(attrs={'type':'file','name':'certificado','id':'certificado','class':'form-control','placeholder':'Introduzca su certificado'}),
            'tipo': forms.Select(attrs={'type':'text','name':'tipo','id':'evento-tipo','class':'form-control required-field', 'placeholder':'Seleccione el tipo de evento'}),
            'modalidad': forms.Select(attrs={'type':'text','name':'organismo','id':'modalidad','class':'form-control required-field', 'placeholder':'Seleccione la modalidad'}),
            'isbn': forms.TextInput(attrs={'type':'text','name':'isbn','id':'isbn','class':'form-control','placeholder':'Introduzca su ISBN'}),
            'area': forms.Select(attrs={'type':'text','name':'area','id':'area','class':'form-control', 'placeholder':'Seleccione'}),
            'departamento': forms.Select(attrs={'type':'text','name':'departamento','id':'departamento','class':'form-control', 'placeholder':'Seleccione'}),
            'institucion': forms.Select(attrs={'type':'text','name':'institucion','id':'evento-institucion','class':'form-control required-field', 'placeholder':'Institución responsable'}),
            'pais': forms.TextInput(attrs={'type':'text','name':'pais','id':'evento-pais','class':'form-control required-field', 'placeholder':'País'}),
            'nombre_ponencia': forms.TextInput(attrs={'type':'text','name':'nombre_ponencia','id':'nombre_ponencia','class':'form-control required-field', 'placeholder':'Nombre de la ponencia'}),
            'provincia': forms.Select(attrs={'type':'text','name':'provincia','id':'evento-provincia','class':'form-control', 'placeholder':'Provincia (solo si es Cuba)'}),
            'url': forms.URLInput(attrs={'type':'text','name':'url','id':'url','class':'form-control', 'placeholder':'URL'}),
            'proyecto': forms.Select(attrs={'class': 'form-control', 'id': 'id_proyecto'})
        }
        date_input_formats = ['%Y-%m-%d']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si estamos editando un evento ya existente
        if self.instance and self.instance.pk:
            valores = []
            for ea in self.instance.eventos_set.all():
                if ea.usuario:
                    valores.append(f"usuario-{ea.usuario.id}")
                elif ea.colaborador:
                    valores.append(f"colaborador-{ea.colaborador.id}")
            self.initial["autores"] = valores


class Proyecto_Form(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = {
            'nombre_proyecto',
            'jefe_proyecto',
            'area',
            'departamento',
            'tipo_proyecto',
            'subtipo_proyecto',
            'entidades_participantes', 
            'sector_estrategico',   
            'linea_investigacion',
            'fecha_inicio',
            'fecha_cierre',
            'estado_proyecto',
            'cantidad_profesores_trabajadores_uho',
            'cantidad_estudiantes_contratados',
            'cantidad_participantes_otras_entidades',
            'cantidad_profesores_colaboradores_uho',
            'cantidad_estudiantes_grupos_cientificos',
            'cantidad_colaboradores_otras_entidades',
            'cantidad_estudiantes_segundo_adelante',
            'cantidad_cuadros_uho',
            'presupuesto_planificado',
            'presupuesto_ejecutado_primer_semestre',
            'presupuesto_ejecutado_segundo_semestre',
        }
        widgets = {
            'nombre_proyecto': forms.TextInput(attrs={'type':'text','name':'nombre_proyecto','id':'nombre_proyecto','class':'form-control', 'placeholder':'Introduzca el nombre del proyecto'}),
            'jefe_proyecto': forms.TextInput(attrs={'type':'text','name':'jefe_proyecto','id':'jefe_proyecto','class':'form-control','placeholder':'Introduzca el Jefe del Proyecto'}),
            'area': forms.Select(attrs={'type':'text','name':'area','id':'area','class':'form-control', 'placeholder':'Seleccione'}),
            'departamento': forms.Select(attrs={'type':'text','name':'departamento','id':'departamento','class':'form-control', 'placeholder':'Seleccione'}),
            'tipo_proyecto': forms.Select(attrs={'type':'text','name':'tipo_proyecto','id':'tipo_proyecto','class':'form-control', 'placeholder':'Seleccione'}),
            'subtipo_proyecto': forms.Select(attrs={'type':'text','name':'subtipo_proyecto','id':'subtipo_proyecto','class':'form-control', 'placeholder':'Seleccione'}),
            'entidades_participantes': forms.Textarea(attrs={'type':'text','name':'entidades_participantes','id':'entidades_participantes','class':'form-control'}),
            'sector_estrategico': forms.Select(attrs={'type':'text','name':'sector_estrategico','id':'sector_estrategico','class':'form-control', 'placeholder':'Seleccione'}),
            'linea_investigacion': forms.Select(attrs={'type':'text','name':'linea_investigacion','id':'linea_investigacion','class':'form-control', 'placeholder':'Seleccione'}),
            'fecha_inicio': forms.DateInput(attrs={'type':'date','name':'fecha_inicio','id':'fecha_inicio','class':'form-control','placeholder':'Introduzca la fecha'}),
            'fecha_cierre': forms.DateInput(attrs={'type':'date','name':'fecha_cierre','id':'fecha_cierre','class':'form-control','placeholder':'Introduzca la fecha'}),
            'estado_proyecto': forms.Select(attrs={'type':'text','name':'estado_proyecto','id':'estado_proyecto','class':'form-control', 'placeholder':'Seleccione'}),
            'cantidad_profesores_trabajadores_uho': forms.NumberInput(attrs={'type':'text','name':'cantidad_profesores_trabajadores_uho','id':'cantidad_profesores_trabajadores_uho','class':'form-control','placeholder':'Introduzca la cantidad de profesores'}),
            'cantidad_estudiantes_contratados': forms.NumberInput(attrs={'type':'text','name':'cantidad_estudiantes_contratados','id':'cantidad_estudiantes_contratados','class':'form-control','placeholder':'Introduzca la cantidad de estudiantes contratados'}),
            'cantidad_participantes_otras_entidades': forms.NumberInput(attrs={'type':'text','name':'cantidad_participantes_otras_entidades','id':'cantidad_participantes_otras_entidades','class':'form-control','placeholder':'Introduzca la cantidad de participantes de otras entidades'}),
            'cantidad_profesores_colaboradores_uho': forms.NumberInput(attrs={'type':'text','name':'cantidad_profesores_colaboradores_uho','id':'cantidad_profesores_colaboradores_uho','class':'form-control','placeholder':'Introduzca la cantidad de profesores colaboradores','required': 'True'}),
            'cantidad_estudiantes_grupos_cientificos': forms.NumberInput(attrs={'type':'text','name':'cantidad_estudiantes_grupos_cientificos','id':'cantidad_estudiantes_grupos_cientificos','class':'form-control','placeholder':'Introduzca la cantidad de estudiantes de GC','required': 'True'}),
            'cantidad_colaboradores_otras_entidades': forms.NumberInput(attrs={'type':'text','name':'cantidad_colaboradores_otras_entidades','id':'cantidad_colaboradores_otras_entidades','class':'form-control','placeholder':'Introduzca la cantidad de otras entidades','required': 'True'}),
            'cantidad_estudiantes_segundo_adelante': forms.NumberInput(attrs={'type':'text','name':'cantidad_estudiantes_segundo_adelante','id':'cantidad_estudiantes_segundo_adelante','class':'form-control','placeholder':'Introduzca la cantidad de estudiante de segundo año en adelante','required': 'True'}),
            'cantidad_cuadros_uho': forms.NumberInput(attrs={'type':'text','name':'cantidad_cuadros_uho','id':'cantidad_cuadros_uho','class':'form-control','placeholder':'Introduzca la cantidad de cuadros de la UHo','required': 'True'}),
            'presupuesto_planificado': forms.NumberInput(attrs={'type':'text','name':'presupuesto_planificado','id':'presupuesto_planificado','class':'form-control','placeholder':'Introduzca el presupuesto planificado','required': 'True'}),
            'presupuesto_ejecutado_primer_semestre': forms.NumberInput(attrs={'type':'text','name':'presupuesto_ejecutado_primer_semestre','id':'presupuesto_ejecutado_primer_semestre','class':'form-control','placeholder':'Introduzca el presupuesto ejecutado en el primer semestre','required': 'True'}),
            'presupuesto_ejecutado_segundo_semestre': forms.NumberInput(attrs={'type':'text','name':'presupuesto_ejecutado_segundo_semestre','id':'presupuesto_ejecutado_segundo_semestre','class':'form-control','placeholder':'Introduzca el presupuesto ejecutado en el segundo semestre','required': 'True'}),
            
        }


class Programa_Form(forms.ModelForm):
    # Campo para entidades participantes
    entidades_participantes = forms.ModelMultipleChoiceField(
        queryset=EntidadParticipante.objects.filter(activo=True),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control entidades-select',
            'data-placeholder': 'Escribir autocompletar',
            'style': 'display: none;'  # Se mostrará como input personalizado
        }),
        required=False
    )
    
    # Campo oculto para participantes UHO
    participantes_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Programa
        fields = [
            'nombre_programa',
            'tipo_programa', 
            'organismo',
            'codigo_programa',
            'entidad_ejecutora',
            'fecha_inicio',
            'fecha_fin',
            'jefe_programa',
            'sector_estrategico',
            'linea_investigacion',
            'entidades_participantes',
            'participantes_data'
        ]
        
        widgets = {
            'nombre_programa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Añadir uno nuevo',
                'required': True
            }),
            'tipo_programa': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'organismo': forms.TextInput(attrs={
                'class': 'form-control autocomplete-field',
                'placeholder': 'Escribir autocompletar',
                'data-field': 'organismo'
            }),
            'codigo_programa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribir código',
                'required': True
            }),
            'entidad_ejecutora': forms.TextInput(attrs={
                'class': 'form-control autocomplete-field',
                'placeholder': 'Escribir autocompletar',
                'data-field': 'entidad_ejecutora'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Año inicio',
                'required': True
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Año fin',
                'required': True
            }),
            'jefe_programa': forms.TextInput(attrs={
                'class': 'form-control autocomplete-field',
                'placeholder': 'Escribir y autocompletar',
                'data-field': 'jefe_programa'
            }),
            'sector_estrategico': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'linea_investigacion': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar querysets
        self.fields['tipo_programa'].queryset = TipoPrograma.objects.filter(activo=True)
        self.fields['sector_estrategico'].queryset = SectorEstrategico.objects.filter(activo=True)
        self.fields['linea_investigacion'].queryset = LineaInvestigacion.objects.filter(activo=True)
        
        # Configurar opciones vacías con placeholders personalizados
        self.fields['tipo_programa'].empty_label = "Escoger tipo programa (CRUD)"
        self.fields['sector_estrategico'].empty_label = "Escoger el sector estratégico (CRUD)"
        self.fields['linea_investigacion'].empty_label = "Escoger línea (CRUD)"
        
        # Preparar datos para autocompletado
        self._prepare_autocomplete_data()
    
    def _prepare_autocomplete_data(self):
        """Preparar datos para campos de autocompletado"""
        # Organismos existentes
        organismos = list(
            Programa.objects.exclude(organismo__exact='')
            .values_list('organismo', flat=True)
            .distinct()
        )
        
        # Entidades ejecutoras existentes
        entidades = list(
            Programa.objects.exclude(entidad_ejecutora__exact='')
            .values_list('entidad_ejecutora', flat=True)
            .distinct()
        )
        
        # Jefes de programa existentes
        jefes = list(
            Programa.objects.exclude(jefe_programa__exact='')
            .values_list('jefe_programa', flat=True)
            .distinct()
        )
        
        # Agregar datos como atributos del widget
        self.fields['organismo'].widget.attrs['data-suggestions'] = json.dumps(organismos)
        self.fields['entidad_ejecutora'].widget.attrs['data-suggestions'] = json.dumps(entidades)
        self.fields['jefe_programa'].widget.attrs['data-suggestions'] = json.dumps(jefes)

    def clean_codigo(self):
        """Validar formato del código"""
        codigo = self.cleaned_data.get('codigo', '').strip().upper()
        if not codigo:
            raise forms.ValidationError("El código es requerido")
        
        # Verificar unicidad
        if Programa.objects.filter(codigo=codigo).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("Ya existe un programa con este código")
        
        return codigo

    def clean_participantes_data(self):
        """Validar datos de participantes"""
        data = self.cleaned_data.get('participantes_data', '')
        if not data:
            return []
        
        try:
            participantes = json.loads(data) if isinstance(data, str) else data
            if not isinstance(participantes, list):
                raise forms.ValidationError("Los datos de participantes deben ser una lista")
            
            # Validar estructura de cada participante
            for participante in participantes:
                if not isinstance(participante, dict):
                    raise forms.ValidationError("Cada participante debe ser un objeto válido")
                if 'usuario_id' not in participante or 'tipo_participacion_id' not in participante:
                    raise forms.ValidationError("Faltan datos requeridos en los participantes")
            
            return participantes
        except (json.JSONDecodeError, TypeError):
            raise forms.ValidationError("Formato de datos de participantes inválido")

    def clean(self):
        cleaned_data = super().clean()
        
        # Validar fechas
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio >= fecha_fin:
                raise forms.ValidationError(
                    "La fecha de inicio debe ser anterior a la fecha de finalización"
                )
        
        return cleaned_data

    def save(self, commit=True):
        programa = super().save(commit=False)
        
        if commit:
            programa.save()
            
            # Guardar relaciones many-to-many
            self.save_m2m()
            
            # Procesar participantes UHO
            participantes_data = self.cleaned_data.get('participantes_data', [])
            if participantes_data:
                self._save_participantes(programa, participantes_data)
        
        return programa
    
    def _save_participantes(self, programa, participantes_data):
        """Guardar participantes UHO"""
        # Limpiar participaciones existentes
        ParticipacionPrograma.objects.filter(programa=programa).delete()
        
        # Crear nuevas participaciones
        for participante_info in participantes_data:
            try:
                usuario = Usuario.objects.get(id=participante_info['usuario_id'])
                tipo_participacion = TipoParticipacion.objects.get(id=participante_info['tipo_participacion_id'])
                
                ParticipacionPrograma.objects.create(
                    programa=programa,
                    usuario=usuario,
                    tipo_participacion=tipo_participacion
                )
            except (Usuario.DoesNotExist, TipoParticipacion.DoesNotExist):
                continue


# Formulario para crear nuevas entidades participantes
class EntidadParticipanteForm(forms.ModelForm):
    class Meta:
        model = EntidadParticipante
        fields = ['nombre', 'sigla', 'tipo_entidad', 'pais']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo de la entidad',
                'required': True
            }),
            'sigla': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sigla (opcional)'
            }),
            'tipo_entidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'Cuba'
            })
        }


# Formulario para crear nuevos tipos de participación
class TipoParticipacionForm(forms.ModelForm):
    class Meta:
        model = TipoParticipacion
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del tipo de participación',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción (opcional)'
            })
        }


class Premio_Form(forms.ModelForm):
    premiados = forms.MultipleChoiceField(
        choices=[],
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control select2', 'style': 'width: 100%;'}
        ),
        required=False
    )

    fecha_create  = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  # <-- necesario para input type="date"
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Introduzca la fecha',
                'name': 'fecha',
                'id': 'fecha',
            }
        ),
        input_formats=['%Y-%m-%d'],  # <-- asegura que Django pueda leer ese formato al editar
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        extra_usuarios = kwargs.pop('extra_usuarios', Usuario.objects.none()) 
        super().__init__(*args, **kwargs)
        
        opciones = []

        # Usuarios
        usuarios = Usuario.objects.exclude(id=user.id) | Usuario.objects.filter(id=user.id)
        usuarios = usuarios | extra_usuarios
        for u in usuarios.distinct():
            opciones.append((f"usuario-{u.id}", f"{u.first_name} {u.last_name}"))

        # Colaboradores
        colaboradores = Colaborador.objects.all()
        for c in colaboradores:
            opciones.append((f"colaborador-{c.id}", f"{c.nombre} {c.apellidos}"))
            
        self.fields['premiados'].choices = opciones
        
       # Establecer initial según si estamos editando o creando
        if self.instance and self.instance.pk:
            # Editando: cargar premiados reales
            premiados_inicial = []
            for p in self.instance.premiados():
                if p.usuario_id:
                    premiados_inicial.append(f"usuario-{p.usuario_id}")
                if p.colaborador_id:
                    premiados_inicial.append(f"colaborador-{p.colaborador_id}")
            self.fields['premiados'].initial = premiados_inicial
        elif user:
            # Creando: marcar usuario actual
            self.fields['premiados'].initial = [f"usuario-{user.id}"]
            
        self.fields['proyecto'].queryset = Proyecto.objects.filter(aprobacion='Aprobado')

        if self.instance.pk is None and self.instance.tipo_id:
            tipo = self.instance.tipo
            if tipo and tipo.institucion_id:
                self.fields['institucion'].initial = tipo.institucion_id

    class Meta:
        model = Premio
        exclude = ['premiados']
        fields = [
            'titulo',
            'fecha_create',
            'premiados',  
            'caracter',
            'tipo',
            'institucion',
            'diploma',
            'proyecto'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Introduzca el título'
            }),
            'caracter': forms.Select(attrs={
                'id': 'id_caracter',
                'class': 'form-control',
                'placeholder': 'Seleccione'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione el tipo de Premio',
                'id': 'id_tipo'
            }),
            'diploma': forms.FileInput(attrs={
                'type':'file',
                'name':'diploma',
                'id':'diploma',
                'class':'form-control',
                'placeholder':'Introduzca su diploma'
            }),
            'fecha_create': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Introduzca la fecha',
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_proyecto'
            })
        }

        
class Perfil_Form(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = {
            'nombre', 
            'apellidos',
            'ci',
            'email',
            'telefono',
            'cargo',
            'categoria_docente',
            'categoria_cientifica',
            'rgate',
            'google_academico',
            'orci',
            'area',
            'departamento',
            'proyecto',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'type':'text','name':'nombre','id':'name','class':'form-control required-field', 'placeholder':'Introduzca su nombre'}),
            'apellidos': forms.TextInput(attrs={'type':'text','name':'apellidos','id':'lastName','class':'form-control required-field','placeholder':'Introduzca sus apellidos'}),
            'ci': forms.NumberInput(attrs={'type':'text','name':'ci','id':'ci','class':'form-control required-field','placeholder':'Introduzca su carnet de identidad'}),
            'email': forms.EmailInput(attrs={'type':'email','name':'email','id':'email','class':'form-control required-field','placeholder':'Introduzca correo electrónico'}),
            'telefono': forms.NumberInput(attrs={'type':'tel','name':'telefono','id':'tel','class':'form-control required-field', 'placeholder':'Introduzca su número de móvil'}),
            'area': forms.Select(attrs={'type':'text','name':'area','id':'area','class':'form-control', 'placeholder':'Seleccione'}),
            'departamento': forms.Select(attrs={'type':'text','name':'departamento','id':'departamento','class':'form-control', 'placeholder':'Seleccione'}),
            'google_academico': forms.URLInput(attrs={'name':'google_academico','id':'google_academico','class':'form-control', 'placeholder':'Introduzca la url', 'required': 'False'}),
            'rgate': forms.URLInput(attrs={'name':'rgate','id':'rgate','class':'form-control', 'placeholder':'Introduzca la url', 'required': 'False'}),
            'categoria_cientifica': forms.Select(attrs={'type':'text','name':'categoria_cientifica','id':'categoria_cientifica','class':'form-control', 'placeholder':'Seleccione', 'required': 'False'}),
            'categoria_docente': forms.Select(attrs={'type':'text','name':'categoria_docente','id':'categoria_docente','class':'form-control', 'placeholder':'Seleccione', 'required': 'False'}),
            'cargo': forms.Select(attrs={'type':'text','name':'cargo','id':'cargo','class':'form-control', 'placeholder':'Introduzca su cargo', 'required': 'False'}),
            'orci': forms.NumberInput(attrs={'type':'text','name':'orci','id':'orci','class':'form-control','placeholder':'Introduzca la ORCI', 'required': 'False'}),
            'proyecto': forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox-list', 'required': 'False'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        
        # Disable area/departamento fields by default
        self.fields['area'].widget.attrs['disabled'] = 'disabled'
        self.fields['departamento'].widget.attrs['disabled'] = 'disabled'
        self.fields['proyecto'].queryset = Proyecto.objects.filter(aprobacion='Aprobado')
        
        # If user has area/departamento, create info fields and set initial values
        if self.user:
            if hasattr(self.user, 'area') and self.user.area:
                self.fields['area'].initial = self.user.area
                self.fields['area_info'] = forms.CharField(
                    label="Área",
                    required=False,
                    initial=self.user.area.nombre_area if hasattr(self.user.area, 'nombre_area') else str(self.user.area),
                    widget=forms.TextInput(attrs={
                        'class': 'form-control readonly-input'
                    })
                )
                
            if hasattr(self.user, 'departamento') and self.user.departamento:
                self.fields['departamento'].initial = self.user.departamento
                self.fields['departamento_info'] = forms.CharField(
                    label="Departamento",
                    required=False,
                    initial=self.user.departamento.nombre_departamento if hasattr(self.user.departamento, 'nombre_departamento') else str(self.user.departamento),
                    widget=forms.TextInput(attrs={
                        'class': 'form-control readonly-input'
                    })
                )
                    

# class BaseArticuloForm(forms.ModelForm):
#     # Campo para seleccionar proyecto (necesario para filtrar colaboradores)
#     proyecto = forms.ModelChoiceField(
#         queryset=Proyecto.objects.filter(aprobacion='Aprobado'),
#         required=False,
#         empty_label="Seleccione un proyecto",
#         widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_proyecto'})
#     )
    
#     colaboradores = forms.ModelMultipleChoiceField(
#         queryset=Colaborador.objects.none(),
#         required=False,
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control',
#             'id': 'id_colaboradores',
#             'multiple': True
#         })
#     )
    
#     class Meta:
#         model = Articulo
#         fields = ['proyecto', 'titulo', 'editorial', 'indexacion', 'fecha_create', 'pais',
#                  'idioma', 'url', 'volumen', 'pag', 'numero', 'colaboradores']
#         widgets = {
#             'titulo': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Introduzca el título'
#             }),
#             'editorial': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Introduzca la editorial'
#             }),
#             'index': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'fecha_creacion': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date'
#             }),
#             'pais': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'idioma': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'url': forms.URLInput(attrs={
#                 'name': 'url',
#                 'id': 'url',
#                 'class': 'form-control', 
#                 'placeholder': 'Introduzca la url'
#             }),
#             'volumen': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Introduzca el volumen'
#             }),
#             'pag': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ej. 12-34'
#             }),
#             'numero': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Introduzca el numero'
#             }),
#             'autores': forms.SelectMultiple(attrs={
#                 'class': 'form-control',
#                 'id': 'id_autores'
#             }),
#         }
    
#     def __init__(self, *args, **kwargs):
#         # Obtener el usuario actual y proyectos si se proporcionan
#         self.user = kwargs.pop('user', None)
#         self.proyectos = kwargs.pop('proyectos', None)
#         super().__init__(*args, **kwargs)
        
#         # Configurar queryset de proyectos si se proporciona
#         if self.proyectos is not None:
#             self.fields['proyecto'].queryset = self.proyectos
        
        
#         # Si tenemos un usuario y estamos creando un nuevo artículo
#         if self.user and not self.instance.pk:
#             # Preseleccionar al usuario actual en el campo de autores
#             if 'autores' in self.initial:
#                 if not isinstance(self.initial['autores'], list):
#                     self.initial['autores'] = [self.initial['autores']]
#                 if self.user.id not in self.initial['autores']:
#                     self.initial['autores'].append(self.user.id)
#             else:
#                 self.initial['autores'] = [self.user.id]
        
#         # Si estamos editando un artículo existente y tiene proyecto
#         if self.instance.pk and hasattr(self.instance, 'proyecto') and self.instance.proyecto:
#             # Filtrar colaboradores por el proyecto del artículo
#             self.fields['colaboradores'].queryset = Colaborador.objects.filter(
#                 proyecto=self.instance.proyecto
#             )
#         # else:
#             # Para nuevos artículos, mostrar todos los colaboradores inicialmente
#             # Se filtrará via JavaScript cuando se seleccione un proyecto
#             # self.fields['colaboradores'].queryset = Colaborador.objects.all()


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            "titulo",
            "doi",
            "issn_isbn",
            "fecha_create",
            "idioma",
            "revista",
            "editorial",
            "volumen",
            "numero",
            "pag",
            "indexacion",
            "url",
            "pais",
            "archivo",
            "forma_citar",
            "proyecto",
            "departamento",
            "area",
        ]
        widgets = {
            "fecha_create": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "idioma": forms.Select(attrs={"class": "form-select"}),
            "revista": forms.Select(attrs={"class": "form-select"}),
            "indexacion": forms.Select(attrs={"class": "form-select"}),
            "proyecto": forms.Select(attrs={"class": "form-select"}),
            "departamento": forms.Select(attrs={"class": "form-select"}),
            "area": forms.Select(attrs={"class": "form-select"}),
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "doi": forms.TextInput(attrs={"class": "form-control"}),
            "issn_isbn": forms.TextInput(attrs={"class": "form-control"}),
            "editorial": forms.TextInput(attrs={"class": "form-control"}),
            "volumen": forms.TextInput(attrs={"class": "form-control"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "pag": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "pais": forms.TextInput(attrs={"class": "form-control"}),
            "archivo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "forma_citar": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # por si quieres filtrar campos según el usuario
        super().__init__(*args, **kwargs)

        # Si quieres inicializar usuario automáticamente y ocultarlo del fo


# class Articulo_Publicacion_Form(BaseArticuloForm):
#     class Meta(BaseArticuloForm.Meta):
#         fields = ['proyecto', 'issn_isbn', 'editorial', 'volumen', 'fecha_create', 
#                  'titulo', 'departamento', 'area', 'pais', 'indexacion', 'forma_citar', 
#                  'pag', 'archivo', 'url', 'idioma', 'numero', 'colaboradores']
        
#         widgets = {
#             **BaseArticuloForm.Meta.widgets,
#             'issn_isbn': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Introduzca el ISBN'
#             }),
#             'capitulo': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Introduzca el capítulo'
#             }),
#             'volumen': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Introduzca el volumen'
#             }),
#             'indexacion': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Seleccione la forma de indexación'
#             }),
#             'forma_citar': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Forma de citar'
#             }),
#             'pag': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ej. 12-34'
#             }),
#             'archivo': forms.ClearableFileInput(attrs={
#                 'class': 'form-control',
#                 'accept': '.pdf,.doc,.docx'
#             })
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['editorial'].widget.attrs.update({
#             'class': 'form-control revista-autocomplete',
#             'autocomplete': 'off'
#         })


class BasesDatosForm(forms.ModelForm):
    class Meta:
        model = Indexacion
        fields = ['nombre_base_datos', 'grupo', 'url']
        widgets = {
            'nombre_base_datos': forms.TextInput(attrs={'class': 'input', 'id': 'id_nombre_base_datos'}),
            'grupo': forms.Select(attrs={'class': 'input', 'id': 'id_grupo'}),
            'url': forms.URLInput(attrs={'class': 'input', 'id': 'id_url'}),
        }
        labels = {
            'nombre_base_datos': 'Nombre de la base de datos',
            'grupo': 'Grupo',
            'url': 'URL',
        }
        
                
class TipoPremioForm(forms.ModelForm):
    class Meta:
        model = TipoPremio
        fields = ['nombre', 'institucion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control required-field'}),
            'institucion': forms.Select(attrs={'class': 'form-control required-field', 'id': 'modal_institucion'}), 
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'institucion'):
            self.fields['institucion'].initial = user.institucion


class CaracterPremioForm(forms.ModelForm):
    class Meta:
        model = CaracterPremio
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control required-field'}),
        }
        
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip().lower()
        if CaracterPremio.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un carácter de premio con ese nombre.")
        return self.cleaned_data['nombre']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
