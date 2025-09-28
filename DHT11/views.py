from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import DHT11Data
from .serializers import DHT11Serializer


class DHT11ViewSet(viewsets.ModelViewSet):
    queryset = DHT11Data.objects.all()
    serializer_class = DHT11Serializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = DHT11Data.objects.all().order_by('-timestamp')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def dht11_frontend(request):
 dados = DHT11Data.objects.all().order_by('-timestamp')[:5]
 return render(request, "DHT11/list.html", {"dados": dados})