from django import forms
from django.forms import ModelForm
from .models import Email, PerfilV
from investigador.models import Articulo, Evento, Programa, Premio, Proyecto
from django.contrib.auth.models import Group, Permission


        
class EmailForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    class Meta:
        model = Email
        fields = '__all__'
        widgets = {
            'address' : forms.EmailInput(attrs={'type':"email",'name':"email", 'class':"input", 'required':'true' ,'id': 'inputEmail'}),
            'smtp_server': forms.TextInput(attrs={'type':"text",'name':"server", 'class':"input", 'id': 'inputServer'}),
            'smtp_port': forms.TextInput(attrs={'type':"text",'name':"port", 'class':"input", 'id': 'inputPort'}),
            'smtp_username': forms.TextInput(attrs={'type':"text",'name':"username", 'class':"input", 'required':'true' ,'id': 'inputUsername'}),
            'smtp_password': forms.TextInput(attrs={'type':"text",'name':"password", 'class':"input", 'required':'true' ,'id': 'inputPassword'}),
        }

class Perfil_Jefedepartamento_Form(forms.ModelForm):
    class Meta:
        model = PerfilV
        fields = {
            'nombre', 
            'apellidos',
            'ci',
            'email',
            'telefono',
            'cargo',
            'categoria_docente',
            'categoria_cientifica',
            'area',
            'departamento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'type':'text','name':'nombre','id':'name','class':'form-control', 'placeholder':'Introduzca su nombre'}),
            'apellidos': forms.TextInput(attrs={'type':'text','name':'apellidos','id':'lastName','class':'form-control','placeholder':'Introduzca sus apellidos'}),
            'ci': forms.NumberInput(attrs={'type':'text','name':'ci','id':'ci','class':'form-control','placeholder':'Introduzca su carnet de identidad'}),
            'email': forms.EmailInput(attrs={'type':'email','name':'email','id':'email','class':'form-control','placeholder':'Introduzca correo electrónico'}),
            'telefono': forms.NumberInput(attrs={'type':'tel','name':'telefono','id':'tel','class':'form-control', 'placeholder':'Introduzca su número de móvil'}),
            'area': forms.Select(attrs={'type':'text','name':'area','id':'area','class':'form-control', 'placeholder':'Seleccione', 'disabled': 'disabled'}),
            'categoria_cientifica': forms.Select(attrs={'type':'text','name':'categoria_cientifica','id':'categoria_cientifica','class':'form-control', 'placeholder':'Seleccione'}),
            'categoria_docente': forms.Select(attrs={'type':'text','name':'categoria_docente','id':'categoria_docente','class':'form-control', 'placeholder':'Seleccione'}),
            'cargo': forms.TextInput(attrs={'type':'text','name':'cargo','id':'cargo','class':'form-control', 'placeholder':'Introduzca su cargo'}),
            'departamento': forms.Select(attrs={'type':'text','name':'departamento','id':'departamento','class':'form-control', 'placeholder':'Seleccione', 'disabled': 'disabled'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si el perfil tiene un usuario asociado, mostrar los valores de área y departamento
        if self.instance and self.instance.usuario:
            if self.instance.usuario.area:
                self.fields['area'].initial = self.instance.usuario.area
                self.fields['area'].widget.attrs['readonly'] = True
                
            if self.instance.usuario.departamento:
                self.fields['departamento'].initial = self.instance.usuario.departamento
                self.fields['departamento'].widget.attrs['readonly'] = True


class Perfil_JefeArea_Form(forms.ModelForm):
    class Meta:
        model = PerfilV
        fields = {
            'nombre', 
            'apellidos',
            'ci',
            'email',
            'telefono',
            'cargo',
            'categoria_docente',
            'categoria_cientifica',
            'area',
            'departamento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'type':'text','name':'nombre','id':'name','class':'form-control', 'placeholder':'Introduzca su nombre'}),
            'apellidos': forms.TextInput(attrs={'type':'text','name':'apellidos','id':'lastName','class':'form-control','placeholder':'Introduzca sus apellidos'}),
            'ci': forms.NumberInput(attrs={'type':'text','name':'ci','id':'ci','class':'form-control','placeholder':'Introduzca su carnet de identidad'}),
            'email': forms.EmailInput(attrs={'type':'email','name':'email','id':'email','class':'form-control','placeholder':'Introduzca correo electrónico'}),
            'telefono': forms.NumberInput(attrs={'type':'tel','name':'telefono','id':'tel','class':'form-control', 'placeholder':'Introduzca su número de móvil'}),
            'area': forms.Select(attrs={'type':'text','name':'area','id':'area','class':'form-control', 'placeholder':'Seleccione', 'disabled': 'disabled'}),
            'categoria_cientifica': forms.Select(attrs={'type':'text','name':'categoria_cientifica','id':'categoria_cientifica','class':'form-control', 'placeholder':'Seleccione'}),
            'categoria_docente': forms.Select(attrs={'type':'text','name':'categoria_docente','id':'categoria_docente','class':'form-control', 'placeholder':'Seleccione'}),
            'cargo': forms.TextInput(attrs={'type':'text','name':'cargo','id':'cargo','class':'form-control', 'placeholder':'Introduzca su cargo'}),
            'departamento': forms.Select(attrs={'type':'text','name':'departamento','id':'departamento','class':'form-control', 'placeholder':'Seleccione', 'disabled': 'disabled'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si el perfil tiene un usuario asociado, mostrar los valores de área y departamento
        if self.instance and self.instance.usuario:
            if self.instance.usuario.area:
                self.fields['area'].initial = self.instance.usuario.area
                self.fields['area'].widget.attrs['readonly'] = True
                
            if self.instance.usuario.departamento:
                self.fields['departamento'].initial = self.instance.usuario.departamento
                self.fields['departamento'].widget.attrs['readonly'] = True

class Perfil_Form_Vicerrector(forms.ModelForm):
    class Meta:
        model = PerfilV
        fields = {
            'nombre', 
            'apellidos',
            'ci',
            'email',
            'telefono',
            'cargo',
            'categoria_docente',
            'categoria_cientifica',
            'area',
            'departamento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'type':'text','name':'nombre','id':'name','class':'form-control', 'placeholder':'Introduzca su nombre'}),
            'apellidos': forms.TextInput(attrs={'type':'text','name':'apellidos','id':'lastName','class':'form-control','placeholder':'Introduzca sus apellidos'}),
            'ci': forms.NumberInput(attrs={'type':'text','name':'ci','id':'ci','class':'form-control','placeholder':'Introduzca su carnet de identidad'}),
            'email': forms.EmailInput(attrs={'type':'email','name':'email','id':'email','class':'form-control','placeholder':'Introduzca correo electrónico'}),
            'telefono': forms.NumberInput(attrs={'type':'tel','name':'telefono','id':'tel','class':'form-control', 'placeholder':'Introduzca su número de móvil'}),
            'categoria_cientifica': forms.Select(attrs={'type':'text','name':'categoria_cientifica','id':'categoria_cientifica','class':'form-control', 'placeholder':'Seleccione'}),
            'categoria_docente': forms.Select(attrs={'type':'text','name':'categoria_docente','id':'categoria_docente','class':'form-control', 'placeholder':'Seleccione'}),
            'cargo': forms.TextInput(attrs={'type':'text','name':'cargo','id':'cargo','class':'form-control', 'placeholder':'Introduzca su cargo'}),
            'area': forms.Select(attrs={'type':'text','name':'area','id':'area','class':'form-control', 'placeholder':'Seleccione', 'disabled': 'disabled'}),
            'departamento': forms.Select(attrs={'type':'text','name':'departamento','id':'departamento','class':'form-control', 'placeholder':'Seleccione', 'disabled': 'disabled'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si el perfil tiene un usuario asociado, mostrar los valores de área y departamento
        if self.instance and self.instance.usuario:
            if self.instance.usuario.area:
                self.fields['area'].initial = self.instance.usuario.area
                self.fields['area'].widget.attrs['readonly'] = True
                
            if self.instance.usuario.departamento:
                self.fields['departamento'].initial = self.instance.usuario.departamento
                self.fields['departamento'].widget.attrs['readonly'] = True

                

                            
class Cambiar_Estado_Articulo_Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    class Meta:
        model = Articulo
        fields = {
            'aprobacion'
        }
        widgets = {
            'aprobacion' : forms.Select(attrs={'class':"form-control", 'id': 'selectEstado'}),   
        }

class Cambiar_Estado_Evento_Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    class Meta:
        model = Evento
        fields = {
            'aprobacion'
        }
        widgets = {
            'aprobacion' : forms.Select(attrs={'class':"form-control", 'id': 'selectEstado'}),   
        }


class Cambiar_Estado_Premio_Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    class Meta:
        model = Premio
        fields = {
            'aprobacion'
        }
        widgets = {
            'aprobacion' : forms.Select(attrs={'class':"form-control", 'id': 'selectEstado'}),   
        }

class Cambiar_Estado_Proyecto_Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    class Meta:
        model = Proyecto
        fields = {
            'aprobacion'
        }
        widgets = {
            'aprobacion' : forms.Select(attrs={'class':"form-control", 'id': 'selectEstado'}),   
        }

class Cambiar_Estado_Programa_Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    class Meta:
        model = Programa
        fields = {
            'aprobacion'
        }
        widgets = {
            'aprobacion' : forms.Select(attrs={'class':"form-control", 'id': 'selectEstado'}),   
        }