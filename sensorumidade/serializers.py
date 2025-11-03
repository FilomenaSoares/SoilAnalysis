from rest_framework import serializers
from .models import sensorumidadeData

class sensorumidadeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = sensorumidadeData
        fields = ('umidadesolo', 'timestampSolo')

# --- CORRIGIDO ---
class sensorumidadeAtualSerializer(serializers.ModelSerializer):
    # Não precisamos renomear o campo, podemos usá-lo diretamente
    # umidade = serializers.FloatField(source='umidadesolo') # <-- REMOVIDO

    class Meta: 
        model = sensorumidadeData
        # Apenas diga ao serializer para usar o campo 'umidadesolo'
        fields = ('umidadesolo',) # <-- CORRIGIDO