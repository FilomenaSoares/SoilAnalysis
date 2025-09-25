from rest_framework import serializers
from DHT11.models import DHT11Data

class DHT11Serializer(serializers.models):
    class meta:
        model:DHT11Data
        fields=('DHT11Id', 'temperatura', 'umidade', 'timestamp', 'topic')

