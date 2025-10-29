from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import sensorumidadeData
from .serializers import sensorumidadeSerializer
import json

class sensorumidadeViewSet(viewsets.ModelViewSet):
    queryset = sensorumidadeData.objects.all()
    serializer_class = sensorumidadeSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = sensorumidadeData.objects.all().order_by('-timestampSolo')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

