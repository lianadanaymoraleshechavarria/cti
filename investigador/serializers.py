from rest_framework import serializers
from .models import Evento, Proyecto, TipoParticipacion


class TipoParticipacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoParticipacion
        fields = ['id', 'nombre']

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'
        
