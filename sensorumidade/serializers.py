from rest_framework import serializers
from sensorumidade.models import sensorumidadeData

class sensorumidadeSerializer(serializers.ModelSerializer):

    class Meta: 
        model = sensorumidadeData
        fields = ('umidadesolo', 'timestampSolo')