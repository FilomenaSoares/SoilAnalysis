from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action  
from .models import DHT11Data
from .serializers import DHT11Serializer, DHT11ChartSerializer 

class DHT11ViewSet(viewsets.ModelViewSet):
    queryset = DHT11Data.objects.all()
    serializer_class = DHT11Serializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def atual(self, request):
        try:
            latest_data = DHT11Data.objects.order_by('-timestamp').first()
            if latest_data:
                serializer = self.get_serializer(latest_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], serializer_class=DHT11ChartSerializer)
    def historico_dia(self, request):
        try:
            queryset = DHT11Data.objects.order_by('-timestamp')[:12]
            
            serializer = self.get_serializer(queryset, many=True)
            
            return Response(list(reversed(serializer.data)), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)