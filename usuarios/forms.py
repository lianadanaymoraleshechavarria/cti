from django import forms
from django.forms import ModelForm
from plataforma.models import Usuario
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


# Formulario de Restablecer Contraseña
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'type':"email",'name':"email", 'class':"input", 'required':'true', 'id': 'email'}),
    )

# Formulario de Cambiar Contraseña
class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("Contraseña"),
        widget=forms.PasswordInput(attrs={"class":"input", "name":"password1", "type":"password","required":"true","id":"password1"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("Repetir Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class":"input", "name":"password2", "type":"password","required":"true", "id":"password2"}),
    )
# Formulario de Usuario
class InformacionPersonalForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'first_name' : forms.TextInput(attrs={'type':"text",'name':"name", 'class':"input", 'required':'true', 'id': 'inputName'}),
            'last_name' : forms.TextInput(attrs={'type':"text",'name':"name", 'class':"input", 'required':'true', 'id': 'inputLastName'}),
            'carnet' : forms.TextInput(attrs={'type':"text",'name':"name", 'class':"input", 'required':'true', 'id': 'inputCi'}),
            'email': forms.EmailInput(attrs={'type':"text",'name':"email", 'class':"input", 'required':'true', 'id': 'inputEmail'}),
            'telefono' : forms.TextInput(attrs={'type':"text",'name':"phone", 'class':"input", 'required':'true', 'id': 'inputNt'}),
            'direccion' : forms.Textarea(attrs={'name':"message", 'class':"input", 'required':'true', 'id': 'inputText'}),

        } 
        
        def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['carnet'].required = False


