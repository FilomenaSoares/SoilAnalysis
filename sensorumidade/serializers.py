from rest_framework import serializers
from .models import sensorumidadeData

class sensorumidadeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = sensorumidadeData
        fields = ('umidadesolo', 'timestampSolo')

class sensorumidadeAtualSerializer(serializers.ModelSerializer):
    umidade = serializers.FloatField(source='umidadesolo')

    class Meta: 
        model = sensorumidadeData
        fields = ('umidade',) 