# dht11_app/apps.py
from django.apps import AppConfig
import os

class Dht11AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensores'

    def ready(self):
        # só inicia MQTT se estivermos rodando o servidor, não para migrate/makemigrations
        if os.environ.get("RUN_MAIN") == "true":  
            from .mqtt_subscriber import start_mqtt
            start_mqtt()
