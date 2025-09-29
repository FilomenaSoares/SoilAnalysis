from django.db import models
from django.utils import timezone

class DHT11Data(models.Model):
    temperatura=models.FloatField()
    umidade=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Sensor {self.sensor_id} - {self.temperatura}°C, {self.umidade}%"