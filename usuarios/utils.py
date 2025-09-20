import os
import logging
import requests
from django.contrib.auth import login, authenticate
from audit.models import LoginLog
# Logger para guardar login en archivo (logs/login.log)
login_logger = logging.getLogger("audit.login")

# Función para registrar intentos de login (DB + archivo)
def log_login_attempt(username, request, auth_mode, success=True, error_msg=None):
    # Guardar en la base de datos
    LoginLog.objects.create(
        username=username,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        auth_mode=auth_mode,
        success=success
    )
    # Guardar en archivo log
    status_text = "EXITOSO" if success else "FALLIDO"
    msg = f"Login {status_text}: usuario={username}, IP={request.META.get('REMOTE_ADDR')}, modo={auth_mode}"
    if error_msg:
        msg += f", error='{error_msg}'"
    login_logger.info(msg)
    
    
# LOCAL authentication
def fetch_user_from_local(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is None:
        return None, "Usuario o contraseña incorrectos"
    return user, None


# SIGENU API authentication
def fetch_user_from_sigenu(username, password):
    try:
        r = requests.post(
            "http://127.0.0.1:8080/api/auth/login/",
            json={"username": username, "password": password},
            timeout=5
        )

        if r.status_code != 200:
            return None, "API externa: credenciales incorrectas"

        data = r.json()
        return data, None

    except requests.RequestException as e:
        return None, f"Error conectando con API externa: {str(e)}"


# UHO API authentication
def fetch_user_from_api_uho(username, password):
    url = "https://auth.uho.edu.cu/login"
    headers = {
        "Origin": "https://auth.uho.edu.cu",  # 👈 cambia al dominio de tu app registrado
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": os.getenv("UHO_AUTH_TOKEN", "AGA tu_token_valido")
    }

    try:
        response = requests.post(url, json={"username": username, "password": password}, headers=headers, timeout=5)

        if response.status_code == 401:
            return None, "Usuario o contraseña incorrectos"
        if response.status_code == 409:
            return None, "Formato inválido al enviar usuario o contraseña"
        if response.status_code >= 500:
            return None, "Error en el servidor de autenticación"

        data = response.json()

        if not data.get("OK") or "activeUser" not in data:
            return None, "Respuesta inválida desde API_UHO"

        user_data = data["activeUser"]
        personal = user_data.get("personal_information", {})
        account_state = user_data.get("account_state", "FALSE")

        return {
            "username": user_data.get("uid"),
            "name": personal.get("given_name"),
            "surname": personal.get("sn"),
            "last_surname": None,
            "identification": personal.get("dni"),
            "email": None,
            "role": user_data.get("status"),  # puedes mapearlo luego a tu rol
            "status": "ACTIVE" if account_state == "TRUE" else "INACTIVE",
            "facultyId": None,
            "townUniversityId": None,
            "personal_photo": personal.get("PersonalPhoto", ''),  # 👈 corregido
        }, None

    except requests.RequestException as e:
        return None, f"Error de conexión: {str(e)}"
    
    
# Actualiza usuario local con datos del API
def update_user_from_api_data(user, data):
    # nombre/apellidos
    user.name = data.get("name") or user.name
    user.surname = data.get("surname") or user.surname
    user.last_surname = data.get("last_surname") or data.get("lastname") or user.last_surname

    # identificación y contacto
    user.identification = data.get("identification") or user.identification
    user.email = data.get("email") or user.email

    # rol/estado/ubicación
    user.role = data.get("role") or user.role      # setter que mapea a 'rol'
    user.status = data.get("status") or user.status
    user.faculty_id = data.get("facultyId") or user.faculty_id
    user.town_university_id = data.get("townUniversityId") or user.town_university_id

    # marca como remoto y valores por defecto de flags
    user.remote_user = True
    user.cancelled = False
    user.blocked = False

    # foto y otros
    user.personal_photo = data.get("personal_photo", user.personal_photo or '')
    # last_login_date lo maneja tu vista con now() cuando se loguea el usuario
    # user.last_login_date = data.get("last_login_date")  # opcional si API lo devuelve

    user.save()


