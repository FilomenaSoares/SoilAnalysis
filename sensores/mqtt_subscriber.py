# dht11_app/mqtt_subscriber.py
import paho.mqtt.client as mqtt

# Configurações do broker
BROKER = "127.0.0.1"  # ou "localhost"
PORT = 1883
TOPIC = "sensors/dht11/#"

def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT com código:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    # Importa o modelo apenas dentro da função
    from .models import DHT11Data
    import json
    try:
        payload = json.loads(msg.payload.decode())
        temperatura = payload.get("temperatura")
        umidade = payload.get("umidade")

        # Salva no banco
        DHT11Data.objects.create(
            temperatura=temperatura,
            humidity=umidade
        )
        print(f"Dados salvos: Temp={temperatura}, Hum={umidade}")
    except Exception as e:
        print("Erro ao salvar dados:", e)

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # roda o loop em background
