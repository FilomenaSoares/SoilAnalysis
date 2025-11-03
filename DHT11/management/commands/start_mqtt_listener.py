import json
import paho.mqtt.client as paho
from paho import mqtt
from django.core.management.base import BaseCommand
from DHT11.models import DHT11Data
from sensorumidade.models import sensorumidadeData  # <-- 1. ADICIONADO

# === CONFIGURAÇÕES DO HiveMQ Cloud ===
MQTT_BROKER = "9e613cab5f6142c582b9bed9e771b713.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
# MQTT_TOPIC = "esp32"  # <-- 2. REMOVIDO (Não é mais necessário, vamos assinar múltiplos)
MQTT_USER = "ESP32"
MQTT_PASSWORD = "EspTeste123"

# --- Funções de callback ---

# 3. FUNÇÃO ON_CONNECT MODIFICADA
def on_connect(client, userdata, flags, rc, properties=None):
    """Chamado quando o cliente se conecta ao broker."""
    if rc == 0:
        print("✅ Conectado ao broker HiveMQ com sucesso!")
        
        # Assinando os tópicos separados
        client.subscribe("esp32/dht11")
        client.subscribe("esp32/umidade_solo")
        
        print("📡 Inscrito nos tópicos: 'esp32/dht11' e 'esp32/umidade_solo'")
    else:
        print(f"❌ Falha na conexão com o broker. Código: {rc}")

# 4. FUNÇÃO ON_MESSAGE MODIFICADA
def on_message(client, userdata, msg):
    """Chamado quando uma mensagem é recebida."""
    try:
        payload = msg.payload.decode("utf-8")
        # Mostra de qual tópico a mensagem veio
        print(f"\n📥 Mensagem recebida no tópico '{msg.topic}': {payload}")
        data = json.loads(payload)

        # --- LÓGICA PARA SEPARAR OS DADOS ---
        if msg.topic == "esp32/dht11":
            temp = data.get("temperatura")
            hum = data.get("umidade")

            if temp is not None and hum is not None:
                DHT11Data.objects.create(temperatura=temp, umidade=hum)
                print(f"💾 Dados (AR) salvos: Temp={temp}°C, Umidade={hum}%")
            else:
                print("⚠️ Mensagem (AR) incompleta, faltando 'temperatura' ou 'umidade'.")
        
        elif msg.topic == "esp32/umidade_solo":
            hum_solo = data.get("umidadesolo")

            if hum_solo is not None:
                sensorumidadeData.objects.create(umidadesolo=hum_solo)
                print(f"💾 Dados (SOLO) salvos: Umidade={hum_solo}%")
            else:
                print("⚠️ Mensagem (SOLO) incompleta, faltando 'umidadesolo'.")

    except Exception as e:
        print(f"🚨 Erro ao processar mensagem: {e}")


class Command(BaseCommand):
    help = 'Listener MQTT para receber dados de ambos os sensores e salvar no banco.'

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