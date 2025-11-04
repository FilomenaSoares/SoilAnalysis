from django.shortcuts import render
import json
from sensorumidade.models import sensorumidadeData
from DHT11.models import DHT11Data
from django.utils import timezone # <-- ADICIONADO

def telainicial(request):
    
    # --- DADOS PARA OS GRÁFICOS ---

    # umidade do solo 
    solo_qs = sensorumidadeData.objects.order_by('-timestampSolo')[:20]
    solo_reverse = list(reversed(solo_qs))
    solo_labels = []
    solo_values = []

    for d in solo_reverse:
        try:
            if d.timestampSolo:
                # CONVERSÃO DE FUSO HORÁRIO ADICIONADA
                local_time_solo = timezone.localtime(d.timestampSolo) 
                hora = local_time_solo.strftime('%H:%M:%S') # <-- CORRIGIDO
            else:
                hora = ""
        except Exception:
            hora = ""
        solo_labels.append(hora)
        solo_values.append(d.umidadesolo or 0)

    # temperatura e umidade do ar (DHT11) 
    ar_qs = DHT11Data.objects.order_by('-timestamp')[:20]
    ar_reverse = list(reversed(ar_qs))
    ar_labels = []
    ar_temp_values = []
    ar_hum_values = []

    for d in ar_reverse:
        try:
            if d.timestamp:
                # CONVERSÃO DE FUSO HORÁRIO ADICIONADA
                local_time_ar = timezone.localtime(d.timestamp)
                hora = local_time_ar.strftime('%H:%M:%S') # <-- CORRIGIDO
            else:
                hora = ""
        except Exception:
            hora = ""
        ar_labels.append(hora)
        ar_temp_values.append(d.temperatura or 0)
        ar_hum_values.append(d.umidade or 0)

    
    # --- DADOS PARA OS CARDS (LÓGICA CORRETA) ---
    latest_ar = DHT11Data.objects.order_by('-timestamp').first()
    latest_solo = sensorumidadeData.objects.order_by('-timestampSolo').first()


    # context enviado p/ template 
    context = {
        # Dados dos gráficos
        'solo_labels': json.dumps(solo_labels),
        'solo_values': json.dumps(solo_values),
        'ar_labels': json.dumps(ar_labels),
        'ar_temp_values': json.dumps(ar_temp_values),
        'ar_hum_values': json.dumps(ar_hum_values),

        # Dados dos cards
        'latest_solo': latest_solo, 
        'latest_ar': latest_ar,
    }

    return render(request, "dashboard_frontend/inicio.html", context)