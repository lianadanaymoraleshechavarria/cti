import uuid
from .forms import InformacionPersonalForm
from plataforma.models import Usuario
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from plataforma.models import Usuario
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, ChangePasswordForm
from plataforma.custom_mail import custom_send_mail
from django.http import JsonResponse
from investigador.models import Area, Departamento
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import AuthenticationSettings
from .serializers import UsuarioSerializer, LoginSerializer
from .utils import (
    log_login_attempt,
    fetch_user_from_local,
    fetch_user_from_sigenu,
    fetch_user_from_api_uho,
    update_user_from_api_data
)
#Login

# def Login(request: HttpRequest):
#     if request.user.is_authenticated:
#         # Redirigir según el rol del usuario ya autenticado
#         return redirect_based_on_role(request.user)
    
#     if request.POST:
#         form_persist = request.POST
#         username = request.POST['username']
#         password = request.POST['password']
        
#         try:
#             user_to_auth = Usuario.objects.get(username=username)
#         except Usuario.DoesNotExist:
#             return render(request, "usuarios/Login.html", {
#                 'response': 'incorrecto', 
#                 'message': "Campos 'Usuario' y 'Contraseña' son incorrectos", 
#                 'form': form_persist
#             })
        
#         user = authenticate(request, username=user_to_auth.username, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirigir según el rol del usuario recién autenticado
#             return redirect_based_on_role(user)
#         else:
#             return render(request, "usuarios/Login.html", {
#                 'response': 'incorrecto', 
#                 'message': 'La información de cuenta no es correcta', 
#                 'form': form_persist
#             })
    
#     return render(request, "usuarios/Login.html")

# views.py
def Login(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Debe ingresar usuario y contraseña")
            return render(request, "usuarios/Login.html", {"form": request.POST})

        try:
            config = AuthenticationSettings.objects.first()
            if not config:
                config = AuthenticationSettings.objects.create(auth_mode='local')
            auth_mode = config.auth_mode
        except Exception as e:
            log_login_attempt(username, request, "N/A", success=False, error_msg=f"Error config: {str(e)}")
            messages.error(request, "Error interno al obtener configuración.")
            return render(request, "usuarios/Login.html", {"form": request.POST})

        user = None
        error = None

        # Local
        if auth_mode == "local":
            user, error = fetch_user_from_local(request, username, password)

        # API SIGENU
        elif auth_mode == "api":
            data, error = fetch_user_from_sigenu(username, password)
            if data:
                user, created = Usuario.objects.get_or_create(username=username)
                update_user_from_api_data(user, data)
                if created:
                    user.set_unusable_password()
                    user.save()

        # API UHO
        elif auth_mode == "api_uho":
            data, error = fetch_user_from_api_uho(username, password)
            if data:
                user, created = Usuario.objects.get_or_create(username=username)
                update_user_from_api_data(user, data)
                if created:
                    user.set_unusable_password()
                    user.save()

        # Si hubo error
        if error:
            log_login_attempt(username, request, auth_mode, success=False, error_msg=error)
            messages.error(request, error)
            return render(request, "usuarios/Login.html", {"form": request.POST})

        # Login exitoso
        if user:
            user.last_login = now()
            user.last_login_ip = request.META.get("REMOTE_ADDR")
            user.save()
            login(request, user)
            log_login_attempt(username, request, auth_mode, success=True)
            return redirect_based_on_role(user)

        # Caso inesperado
        log_login_attempt(username, request, auth_mode, success=False, error_msg="Error de autenticación desconocido")
        messages.error(request, "Error de autenticación")
        return render(request, "usuarios/Login.html", {"form": request.POST})

    return render(request, "usuarios/Login.html", {"form": {}})

def redirect_based_on_role(user):
    """Función auxiliar para redirigir según el rol del usuario"""
    if user.is_superuser or user.rol == 'Administrador':
        return redirect("Dashboard_Admin")
    elif user.rol == 'Vicerrector':
        return redirect("Dashboard_Vicerrector")
    elif user.rol == 'Jefe_departamento':
        return redirect("Dashboard_JefeDepartamento")
    elif user.rol == 'Jefe_area':
        return redirect("Dashboard_JefeArea")
    elif user.rol == 'Investigador':
        return redirect("Dashboard_Investigador")
    else:
        # Redirección por defecto si el rol no está definido
        return redirect("Dashboard_Investigador")  # o la página que consideres adecuada
        
def get_departamentos(request):
    """Obtiene los departamentos filtrados por área en formato JSON"""
    area_id = request.GET.get('area_id')
    departamentos = Departamento.objects.filter(area_id=area_id).values('id', 'nombre_departamento')
    return JsonResponse(list(departamentos), safe=False)

def Registrar(request: HttpRequest):
    # Obtener todas las áreas para el select
    areas = Area.objects.all()
    
    if request.method == 'POST':
        form_data = request.POST.copy()  # Creamos una copia mutable
        
        # Validaciones básicas
        username = form_data.get('username')
        email = form_data.get('email')
        password1 = form_data.get('password1')
        password2 = form_data.get('password2')
        area_id = form_data.get('area')
        departamento_id = form_data.get('departamento')
        
        # Validar usuario único
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya está registrado.')
            return render(request, "usuarios/Registrar.html", {
                'areas': areas,
                'form_data': form_data
            })
        
        # Validar email único
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
            return render(request, "usuarios/Registrar.html", {
                'areas': areas,
                'form_data': form_data
            })
        
        # Validar contraseñas
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, "usuarios/Registrar.html", {
                'areas': areas,
                'form_data': form_data
            })
        
        # Validar área y departamento
        try:
            area = Area.objects.get(id=area_id)
            departamento = Departamento.objects.get(id=departamento_id, area=area)
        except (Area.DoesNotExist, Departamento.DoesNotExist):
            messages.error(request, 'Selección de área o departamento inválida.')
            return render(request, "usuarios/Registrar.html", {
                'areas': areas,
                'form_data': form_data
            })
        

        try:
            usuario = Usuario.objects.create_user(
                username=username,
                email=email,
                password=password1,
                area=area,
                departamento=departamento,
                rol=form_data.get('NombreRol', 'Investigador'),
                telefono=form_data.get('telefono', ''),
                direccion=form_data.get('direccion', ''),
                first_name=form_data.get('first_name', ''),
                last_name=form_data.get('last_name', ''),
                is_active=True  # Cambiar cuando teng acc por email activo, no olvidar 
            )
            
            messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
            return redirect('Login')
            
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, "usuarios/Registrar.html", {
                'areas': areas,
                'form_data': form_data
            })
    
    # GET request - mostrar formulario vacío
    return render(request, "usuarios/Registrar.html", {
        'areas': areas
    })



# Confirmacion del Token de acceso
def TokenValidationView(request, token):
    try:
        usuario = Usuario.objects.get(token_activacion=token)
        
        if usuario.is_active:
            messages.info(request, 'Su cuenta ya está verificada')
            return redirect('Login')
            
        usuario.is_active = True
        usuario.save()
        messages.success(request, '¡Cuenta verificada con éxito!')
        return redirect('Login')
        
    except ObjectDoesNotExist:
        messages.error(request, 'Token inválido o cuenta no encontrada')
        return redirect('Login')
    except Exception as e:
        print(f"Error en activación de cuenta: {e}")
        messages.error(request, 'Error al activar la cuenta. Por favor intente nuevamente.')
        return redirect('Login')

# Restablecer Contraseña
class RestablecerContraseña(auth_views.PasswordResetView):
    template_name = "usuarios/Restablecer Contraseña.html"
    form_class = CustomPasswordResetForm

# Cambiar Contraseña
class CambiarContraseña(auth_views.PasswordResetConfirmView):
    form_class = ChangePasswordForm
    template_name = "usuarios/Cambiar Contraseña.html"

# Confirmacion del Restablecer Contraseña  
def RestablecerContraseñaConfirmado(request):
    return render(request,"usuarios/Restablecer Contraseña Confirmado.html")

# Confirmación del Cambiar Contraseña
def CambiarContraseñaConfirmado(request):
    return render(request,"usuarios/Cambiar Contraseña Confirmado.html")

# Cerrar Sesión
@login_required
def CerrarSesion(request:HttpRequest):
    logout(request)
    return redirect("Login")







