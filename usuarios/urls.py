from django.urls import path
from usuarios import views 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('registrar/', views.Registrar, name='Registrar'),
    path('activar/<str:token>/', views.TokenValidationView, name='activar_cuenta'),
    path('', views.Login, name="Login"),
    path('CerrarSesion/',login_required(views.CerrarSesion), name="CerrarSesion"), 
     path('get_departamentos/', views.get_departamentos, name='get_departamentos'),
    # Contraseña Olvidada
    path('verify/<token>', views.TokenValidationView , name="token_verify"),
    path('reset_password/', views.RestablecerContraseña.as_view() , name="password_reset"),
    path('reset_password_send/', views.RestablecerContraseñaConfirmado, name="password_reset_done"),
    path('reset/<uidb64>/<token>', views.CambiarContraseña.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', views.CambiarContraseñaConfirmado, name="password_reset_complete"),

]