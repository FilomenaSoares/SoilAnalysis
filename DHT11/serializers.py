from rest_framework import serializers
from .models import DHT11Data
from django.utils import timezone  # <-- 1. ADICIONE ESTA IMPORTAÇÃO

class DHT11Serializer(serializers.ModelSerializer):
    class Meta:
        model = DHT11Data
        fields = ('temperatura', 'umidade', 'timestamp')

class DHT11ChartSerializer(serializers.ModelSerializer):
    hora = serializers.SerializerMethodField()

    class Meta:
        model = DHT11Data
        fields = ('temperatura', 'umidade', 'hora')

    def get_hora(self, obj):
        # 2. CORREÇÃO APLICADA AQUI
        # Converte o timestamp UTC para o fuso horário local do seu servidor
        local_time = timezone.localtime(obj.timestamp)
        # Formata a hora local convertida
        return local_time.strftime('%H:%M')