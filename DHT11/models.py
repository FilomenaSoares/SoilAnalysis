from django.db import models

class DHT11Data(models.Model):
    sensor_id = models.CharField(max_length=50, null=True, blank=True)
    topic = models.CharField(max_length=255, null=True)
    temperatura=models.FloatField()
    umidade=models.FloatField()
    timestamp=models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Sensor {self.sensor_id} - {self.temperature}°C, {self.humidity}%"