from rest_framework import serializers
from .models import DHT11Data

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
        return obj.timestamp.strftime('%H:%M')