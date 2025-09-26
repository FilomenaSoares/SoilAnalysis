from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from DHT11.models import DHT11Data
from DHT11.serializers import DHT11Serializer
from rest_framework import routers, serializers, viewsets, permissions


from .models import DHT11Data
from .serializers import DHT11Serializer

class DHT11ViewSet(viewsets.ModelViewSet):
    queryset = DHT11Data.objects.all()
    serializer_class = DHT11Serializer
    permission_classes = [permissions.AllowAny]

#listagem dos dados do sensor
@api_view(['GET', 'POST'])
def dht11_list(request, format=None):

    if request.method == 'GET':
        DHT11 = DHT11.objects.all().order_by('-timestamp')[:5]
        serializer = DHT11Serializer(DHT11, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DHT11Serializer (data=request.data)
        if serializer.id_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTPP_400_BAD_REQUEST)

     