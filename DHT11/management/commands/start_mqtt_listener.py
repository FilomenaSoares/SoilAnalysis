import json
import paho.mqtt.client as paho
from paho import mqtt
from django.core.management.base import BaseCommand
from DHT11.models import DHT11Data  

# === CONFIGURAÇÕES DO HiveMQ Cloud ===
MQTT_BROKER = ""  
MQTT_PORT = 8883
MQTT_TOPIC = "esp32/dados"  # mesmo tópico que o ESP32 publica
MQTT_USER = ""
MQTT_PASSWORD = ""

# --- Funções de callback ---

def on_connect(client, userdata, flags, rc, properties=None):
    """Chamado quando o cliente se conecta ao broker."""
    if rc == 0:
        print("✅ Conectado ao broker HiveMQ com sucesso!")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Inscrito no tópico: '{MQTT_TOPIC}'")
    else:
        print(f"❌ Falha na conexão com o broker. Código: {rc}")

def on_message(client, userdata, msg):
    """Chamado quando uma mensagem é recebida."""
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


class Command(BaseCommand):
    help = 'Listener MQTT para receber dados do sensor DHT11 e salvar no banco.'

    def handle(self, *args, **options):
        # Cliente MQTT com ID único
        client = paho.Client(client_id="django_listener", userdata=None, protocol=paho.MQTTv5)
        client.on_connect = on_connect
        client.on_message = on_message

        # TLS seguro (HiveMQ Cloud exige TLS)
        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # Para testes locais, aceita certificado inseguro
        client.tls_insecure_set(True)

        # Autenticação
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

        self.stdout.write(self.style.SUCCESS("🔄 Conectando ao broker HiveMQ..."))
        client.connect(MQTT_BROKER, MQTT_PORT)

        try:
            client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("\n🛑 Desconectando do broker..."))
            client.disconnect()
            self.stdout.write(self.style.SUCCESS("👋 Cliente desconectado."))
