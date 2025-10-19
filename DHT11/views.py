from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import DHT11Data
from .serializers import DHT11Serializer
import json

class DHT11ViewSet(viewsets.ModelViewSet):
    queryset = DHT11Data.objects.all()
    serializer_class = DHT11Serializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = DHT11Data.objects.all().order_by('-timestamp')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def dht11_frontend(request):
    latest_data = DHT11Data.objects.order_by('-timestamp')[:20]
    
    chart_data = reversed(list(latest_data))

    labels = []
    temperatures = []
    humidities = []

    for data in chart_data:
        labels.append(data.timestamp.strftime('%H:%M:%S'))
        temperatures.append(data.temperatura)
        humidities.append(data.umidade)

    context = {
        'latest_data': latest_data, 
        'labels_json': json.dumps(labels),
        'temperatures_json': json.dumps(temperatures),
        'humidities_json': json.dumps(humidities),
    }
    
    return render(request, "DHT11/list.html", context)

