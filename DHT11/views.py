from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DHT11Data
from .serializers import DHT11Serializer, DHT11ChartSerializer
# (Não precisamos de imports novos)

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

    # --- FUNÇÃO DO GRÁFICO MODIFICADA ---
    @action(detail=False, methods=['get'], serializer_class=DHT11ChartSerializer)
    def historico_dia(self, request):
        try:
            # 1. Define quantos pontos queremos no gráfico (ex: 12 pontos)
            PONTOS_NO_GRAFICO = 12

            # 2. Define o período (ex: últimas 2 horas)
            # 12 pontos/min * 60 min/h * 2 horas = 1440 pontos
            # (Vamos buscar 1500 para ter margem)
            PONTOS_TOTAIS_BUSCADOS = 1500 

            # 3. Calcula o intervalo da amostragem
            # 1500 / 12 = 125
            INTERVALO_AMOSTRAGEM = PONTOS_TOTAIS_BUSCADOS // PONTOS_NO_GRAFICO

            # 4. Busca os dados recentes do banco
            todos_dados_recentes = DHT11Data.objects.order_by('-timestamp')[:PONTOS_TOTAIS_BUSCADOS]

            # 5. Faz a amostragem (sampling)
            # Pega 1 ponto a cada 'INTERVALO_AMOSTRAGEM'
            dados_amostrados = list(todos_dados_recentes)[::INTERVALO_AMOSTRAGEM]
            
            # 6. Serializa os dados amostrados
            serializer = self.get_serializer(dados_amostrados, many=True)
            
            # 7. Retorna a lista na ordem correta (antigo -> novo)
            return Response(list(reversed(serializer.data)), status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)