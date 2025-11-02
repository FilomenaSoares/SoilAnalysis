from django.db import models

class DHT11Data(models.Model):
    temperatura = models.FloatField()
    umidade = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.temperatura}°C, {self.umidade}%"