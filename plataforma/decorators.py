from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from .choices import ROLES_USUARIO

def get_rol_display(user):
    """Obtiene el nombre a mostrar del rol del usuario"""
    return dict(ROLES_USUARIO).get(user.rol, user.rol)

def role_required(*roles, redirect_url='Dashboard_Investigador'):
    """
    Decorador genérico para requerir uno de varios roles
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Verifica si el usuario tiene alguno de los roles requeridos
                if request.user.rol in roles or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
            
            # Usuario no autenticado o sin los roles necesarios
            if redirect_url:
                return redirect(redirect_url)
            raise PermissionDenied
        return _wrapped_view
    return decorator

# Decoradores específicos basados en el decorador genérico

def admin_required(function):
    return role_required('Administrador')(function)

def pure_admin_required(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
            
        if request.user.is_superuser or request.user.rol == 'Administrador':
            return function(request, *args, **kwargs)
            
        return redirect('Dashboard_Investigador')
    return _wrapped_view

def vicedecano_required(function):
    return role_required('Vicedecano')(function)

def vicerrector_required(function):
    return role_required('Vicerrector')(function)

def investigador_required(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
            
        if request.user.rol == 'Investigador':
            return function(request, *args, **kwargs)
            
        raise PermissionDenied(get_rol_display(request.user))
    return _wrapped_view

def jefearea_required(function):
    return role_required('Jefe_area', 'jefe de area')(function)

def jefedepartamento_required(function):
    return role_required('Jefe_departamento')(function)

# Decorador adicional para múltiples roles
def roles_required(*roles):
    """Decorador que permite especificar qué roles pueden acceder"""
    return role_required('Jefe_area', 'Jefe_departamento','Vicerrector')


def admin_staff_required(function):
    """Requiere cualquier rol administrativo (Administrador, Jefe de Área/Departamento, Vicerrector)"""
    return role_required(
        'Administrador',
        'Jefe_area', 
        'Jefe de Area',
        'Jefe área',
        'Jefe_departamento',
        'Jefe de Departamento',
        'Vicerrector'
    )(function)


    


   