from rest_framework import serializers
from .models import Estadistica

class EstadisticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadistica
        fields = '__all__'