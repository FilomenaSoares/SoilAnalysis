from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action  
from .models import sensorumidadeData
from .serializers import sensorumidadeSerializer, sensorumidadeAtualSerializer
import json

class sensorumidadeViewSet(viewsets.ModelViewSet):
    queryset = sensorumidadeData.objects.all()
    serializer_class = sensorumidadeSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def atual(self, request):
        try:
            latest_data = sensorumidadeData.objects.order_by('-timestampSolo').first()
            
            if latest_data:
                serializer = sensorumidadeAtualSerializer(latest_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_4_NOT_FOUND)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
