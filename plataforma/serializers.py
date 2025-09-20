from rest_framework import serializers
from .models import Noticias

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticias
        exclude = ['on_create','on_modified']