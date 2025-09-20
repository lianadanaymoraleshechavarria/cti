from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import AbstractUser
from .choices import  ROLES_BASE

class Email(models.Model):
    address = models.EmailField(unique=True)
    smtp_server = models.CharField(max_length=255)
    smtp_port = models.CharField(max_length=3)
    smtp_username = models.CharField(max_length=255)
    smtp_password = models.CharField(max_length=255)

    def __str__(self):
        return self.address

class NombreRol(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre_personalizado = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Nombre de Rol"
        verbose_name_plural = "Nombres de Roles"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('roles_personalizados_cache')


class Usuario(AbstractUser):
    token_activacion = models.CharField(max_length=100, blank=True, null=True)
    carnet = models.CharField(max_length=11, unique=False, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    area = models.ForeignKey(
        'investigador.Area',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    departamento = models.ForeignKey(
        'investigador.Departamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    rol = models.CharField(
        max_length=20,
        choices=ROLES_BASE,
        blank=False,
        null=False,
        verbose_name='Rol de Usuario',
        default='Investigador'
    )

    # --- Campos añadidos desde Xuser para compatibilidad ---
    identification = models.CharField(max_length=1024, blank=True, null=True)
    personal_photo = models.TextField(blank=True, null=True)   # base64 o URL
    status = models.CharField(max_length=64, blank=True, null=True)
    faculty_id = models.CharField(max_length=64, blank=True, null=True)
    town_university_id = models.CharField(max_length=64, blank=True, null=True)
    cancelled = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    remote_user = models.BooleanField(default=False)
    last_login_ip = models.CharField(max_length=1024, blank=True, null=True)
    question = models.CharField(max_length=1024, blank=True, null=True)
    last_surname = models.CharField(max_length=1024, blank=True, null=True)

    # no cambiamos el PK ni el USERNAME_FIELD (se mantiene como en AbstractUser)

    def __str__(self):
        return self.username

    # --- Propiedades para compatibilidad con código que espera name/surname/role/last_login_date ---
    @property
    def name(self):
        return self.first_name or ''

    @name.setter
    def name(self, value):
        self.first_name = value or ''

    @property
    def surname(self):
        return self.last_name or ''

    @surname.setter
    def surname(self, value):
        self.last_name = value or ''

    @property
    def role(self):
        # Mapear role a tu campo 'rol'
        return self.rol

    @role.setter
    def role(self, value):
        self.rol = value

    @property
    def last_login_date(self):
        # reutiliza el campo `last_login` de AbstractUser
        return self.last_login

    @last_login_date.setter
    def last_login_date(self, value):
        self.last_login = value

    # --- Métodos de ayuda de rol (ajusta strings según tus códigos reales en ROLES_BASE) ---
    def is_secretary(self):
        r = (self.rol or "").upper()
        return r in ("SECRETARY", "SECRETARIA", "SECRETARÍA")

    def is_professor(self):
        r = (self.rol or "").upper()
        return r in ("PROFESSOR", "PROFESOR")

    def is_student(self):
        r = (self.rol or "").upper()
        return r in ("STUDENT", "ESTUDIANTE")

    def is_coordinator(self):
        r = (self.rol or "").upper()
        return r in ("COORDINATOR", "COORDINADOR")
            
class PerfilV(models.Model):
    marcador = 'PerfilV'
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=False, null=False)
    apellidos = models.CharField(max_length=150, blank=False, null=False)
    ci = models.CharField(max_length=11, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    telefono = models.CharField(max_length=8, blank=False, null=False)
    cargo = models.CharField(max_length=100, blank=False, null=False)
    categoria_docente = models.ForeignKey('investigador.Categoria_docente', on_delete=models.SET_NULL, null=True, blank=True)
    categoria_cientifica = models.ForeignKey('investigador.Categoria_cientifica', on_delete=models.SET_NULL, null=True, blank=True)
    area = models.ForeignKey('investigador.Area', on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey('investigador.Departamento', on_delete=models.SET_NULL, null=True, blank=True)

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