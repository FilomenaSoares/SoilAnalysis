import os
import sys
import json
import django
import paho.mqtt.client as paho
from paho import mqtt

# --- Configuração do Django ---
# Garante que o script consiga acessar os models e o banco de dados do seu projeto.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soilanalysis.settings")
django.setup()

# --- Importação do Model ---
# IMPORTANTE: Verifique se o nome do seu app é 'DHT11' e o nome do model é 'DHT11Data'.
# Se for diferente (ex: app 'users' e model 'SensorData'), você precisa corrigir esta linha.
from DHT11.models import DHT11Data

# === Suas Configurações Corretas do HiveMQ ===
MQTT_BROKER = "9e613cab5f6142c582b9bed9e771b713.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "esp32"  # Tópico correto que o seu ESP32 está usando
MQTT_USER = "ESP32"
MQTT_PASSWORD = "EspTeste123"

# --- Funções de Callback ---

def on_connect(client, userdata, flags, rc, properties=None):
    """Função chamada quando o cliente se conecta."""
    if rc == 0:
        print("✅ Conectado ao broker HiveMQ com sucesso!")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Inscrito no tópico: '{MQTT_TOPIC}'")
    else:
        print(f"❌ Falha na conexão com o broker. Código: {rc}")

def on_message(client, userdata, msg):
    """Função chamada quando uma mensagem é recebida."""
    try:
        payload = msg.payload.decode("utf-8")
        print(f"\n📥 Mensagem recebida: {payload}")
        
        data = json.loads(payload)
        
        # --- CORREÇÃO: Usando as chaves em português que o seu ESP32 envia ---
        temp = data.get("temperatura")
        hum = data.get("umidade")

        if temp is not None and hum is not None:
            # Salva os dados no banco de dados usando o model DHT11Data
            DHT11Data.objects.create(
                temperatura=temp,
                umidade=hum
                # O timestamp será adicionado automaticamente pelo Django se o model estiver configurado com auto_now_add=True
            )
            print(f"💾 Dados salvos: Temp={temp}°C, Umidade={hum}%")
        else:
            print("⚠️ Mensagem incompleta, faltando 'temperatura' ou 'umidade'.")

    except Exception as e:
        print(f"🚨 Erro ao processar mensagem: {e}")

# --- Configuração do Cliente MQTT ---
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

# Configurações de segurança TLS e credenciais
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD) # Suas credenciais

print("🔄 Conectando ao broker HiveMQ...")
client.connect(MQTT_BROKER, MQTT_PORT)

# Mantém o script rodando para ouvir as mensagens
client.loop_forever()
