from django.shortcuts import render
import json
from sensorumidade.models import sensorumidadeData
from DHT11.models import DHT11Data


def telainicial(request):

    solo_qs = sensorumidadeData.objects.order_by('-timestampSolo')[:20]
    solo_reverse = list(reversed(solo_qs))
    solo_labels = []
    solo_values = []

    for d in solo_reverse:
        solo_labels.append(d.timestampSolo.strftime('%H:%M:%S') if d.timestampSolo else "")
        solo_values.append(d.umidadesolo or 0)

    
    ar_qs = DHT11Data.objects.order_by('-timestamp')[:20]
    ar_reverse = list(reversed(ar_qs))
    ar_labels = []
    ar_temp_values = []
    ar_hum_values = []

    for d in ar_reverse:
        ar_labels.append(d.timestamp.strftime('%H:%M:%S') if d.timestamp else "")
        ar_temp_values.append(d.temperatura or 0)
        ar_hum_values.append(d.umidade or 0)

    context = {
        'solo_labels': json.dumps(solo_labels),
        'solo_values': json.dumps(solo_values),
        'ar_labels': json.dumps(ar_labels),
        'ar_temp_values': json.dumps(ar_temp_values),
        'ar_hum_values': json.dumps(ar_hum_values),
        'last_solo': solo_qs,
        'last_ar': ar_qs,
    }

    return render(request, "dashboard_frontend/inicio.html", context)
