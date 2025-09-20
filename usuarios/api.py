from plataforma.models import Usuario
from rest_framework import viewsets, permissions
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UsuarioSerializer