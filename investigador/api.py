from .models import Evento
from rest_framework import viewsets, permissions
from .serializers import EventoSerializer

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EventoSerializer
    
