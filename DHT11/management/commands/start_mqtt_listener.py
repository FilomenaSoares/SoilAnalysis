import json
import paho.mqtt.client as paho
from paho import mqtt
from django.core.management.base import BaseCommand

# --- IMPORTANTE: Importação do Model ---
# O seu projeto tem dois apps que podem guardar os dados: 'DHT11' e 'users'.
# O script original usava 'DHT11.models'. Vamos manter isso.
# Se der um erro de importação, provavelmente teremos que mudar para 'from users.models import ...'
from DHT11.models import DHT11Data

# === Suas Configurações Corretas do HiveMQ ===
MQTT_BROKER = "9e613cab5f6142c582b9bed9e771b713.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "esp32"
MQTT_USER = "ESP32"
MQTT_PASSWORD = "EspTeste123"

# --- Funções de Callback (exatamente como antes) ---

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
        temp = data.get("temperatura")
        hum = data.get("umidade")

        if temp is not None and hum is not None:
            DHT11Data.objects.create(temperatura=temp, umidade=hum)
            print(f"💾 Dados salvos: Temp={temp}°C, Umidade={hum}%")
        else:
            print("⚠️ Mensagem incompleta, faltando 'temperatura' ou 'umidade'.")
    except Exception as e:
        print(f"🚨 Erro ao processar mensagem: {e}")

# --- Classe do Comando Django ---
# Esta é a estrutura que faz o script funcionar como um comando do manage.py
class Command(BaseCommand):
    help = 'Inicia o listener MQTT para receber dados do sensor e salvar no banco de dados.'

    def handle(self, *args, **options):
        client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        client.on_connect = on_connect
        client.on_message = on_message

        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

        self.stdout.write(self.style.SUCCESS("🔄 Conectando ao broker HiveMQ..."))
        client.connect(MQTT_BROKER, MQTT_PORT)

        try:
            client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("\n🛑 Desconectando do broker..."))
            client.disconnect()
            self.stdout.write(self.style.SUCCESS("👋 Cliente desconectado."))

