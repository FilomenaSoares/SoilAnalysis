# mqtt_client.py

import time
import ssl
import paho.mqtt.client as paho
from paho import mqtt
import sys
import os
import json
from datetime import datetime

# Configurando o Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soilanalysis.settings")

import django
django.setup()

from DHT11.models import DHT11Data  # Importa seu modelo Django

# ========== CONFIGURAÇÕES DO MQTT ==========
MQTT_BROKER = "SUA_URL_DO_BROKER"         # Ex: "abc123.s2.eu.hivemq.cloud"
MQTT_PORT = 8883                          # Porta segura padrão para MQTT com TLS
MQTT_USERNAME = "seu_usuario"
MQTT_PASSWORD = "sua_senha"
MQTT_TOPIC = "sensores/dht11"            # Altere para o tópico usado pelo sensor
# ============================================

# Callback de conexão
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(" Conectado com sucesso ao broker MQTT")
        client.subscribe(MQTT_TOPIC, qos=1)
    else:
        print(f" Falha na conexão. Código: {rc}")

# Callback de mensagem recebida
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        temp = data.get("temperature")
        hum = data.get("humidity")

        if temp is not None and hum is not None:
            DHT11Data.objects.create(
                temperatura=temp,
                umidade=hum,
                timestamp=datetime.now()
            )
            print(f" Dados salvos: Temp={temp}°C, Hum={hum}%, Timestamp={datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        else:
            print(" Dados incompletos ou inválidos recebidos.")
    except Exception as e:
        print(f" Erro ao processar mensagem: {e}")

# Callback de inscrição
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f" Inscrito no tópico: {MQTT_TOPIC} com QoS {granted_qos[0]}")

# Callback de publicação (caso publique algo)
def on_publish(client, userdata, mid, properties=None):
    print(f"Mensagem publicada. mid: {mid}")

# Criação do cliente MQTT
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish

# Configura TLS (conexão segura com HiveMQ Cloud)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)

# Autenticação
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Conecta ao broker
client.connect(MQTT_BROKER, MQTT_PORT)

# Inicia o loop
client.loop_forever()
