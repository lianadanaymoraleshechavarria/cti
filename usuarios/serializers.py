from rest_framework import serializers
from django.contrib.auth import authenticate
from plataforma.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'rol', 'telefono', 'direccion', 'carnet',
            'area', 'departamento'
        ]
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Autenticación usando Django
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo")

        # Se pueden agregar verificaciones por rol si es necesario
        # Ejemplo: solo permitir ciertos roles
        # if user.rol not in ['Investigador', 'Administrador']:
        #     raise serializers.ValidationError("Rol no permitido")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # Retorna el usuario autenticado
        return validated_data['user']

    def update(self, instance, validated_data):
        return instance
