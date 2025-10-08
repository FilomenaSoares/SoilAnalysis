from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import DHT11Data
from .serializers import DHT11Serializer
import json # Importa a biblioteca JSON

# --- Esta parte (ViewSet) permanece intacta ---
class DHT11ViewSet(viewsets.ModelViewSet):
    queryset = DHT11Data.objects.all()
    serializer_class = DHT11Serializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = DHT11Data.objects.all().order_by('-timestamp')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# --- É AQUI QUE FAZEMOS A MÁGICA ---
def dht11_frontend(request):
    # Pega os últimos 20 registros do banco de dados para ter um bom histórico no gráfico
    latest_data = DHT11Data.objects.order_by('-timestamp')[:20]
    
    # Invertemos a ordem para que o gráfico mostre do mais antigo para o mais novo
    chart_data = reversed(list(latest_data))

    # --- PREPARAÇÃO DOS DADOS PARA O GRÁFICO ---
    # Cria as listas que o Chart.js vai usar
    labels = []
    temperatures = []
    humidities = []

    for data in chart_data:
        labels.append(data.timestamp.strftime('%H:%M:%S'))
        temperatures.append(data.temperatura)
        humidities.append(data.umidade)

    # Prepara o "pacote" de dados que será enviado para a página HTML
    context = {
        # 'dados' agora se chama 'latest_data' para ficar mais claro
        'latest_data': latest_data, 
        'labels_json': json.dumps(labels),
        'temperatures_json': json.dumps(temperatures),
        'humidities_json': json.dumps(humidities),
    }
    
    # Envia os dados para o template renderizar
    return render(request, "DHT11/list.html", context)

