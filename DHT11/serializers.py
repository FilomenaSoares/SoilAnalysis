from rest_framework import serializers
from DHT11.models import DHT11Data

class DHT11Serializer(serializers.ModelSerializer):
    class Meta:
        model = DHT11Data
        fields = ('temperatura', 'umidade', 'timestamp')

