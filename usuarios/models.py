import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class AuthenticationSettings(models.Model):
    AUTH_CHOICES = [
        ("local", "LOCAL"),
        ("api", "API SIGENU"),
        ("api_uho", "API UHO"),
    ]
    auth_mode = models.CharField(max_length=10, choices=AUTH_CHOICES, default="local")

    class Meta:
        db_table = "authentication_settings"

    def __str__(self):
        return f"Modo de autenticación: {self.auth_mode}"

