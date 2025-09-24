from django.db import models

class DHT11Data(models.Model):

    temperatura=models.FloatField()
    umidade=models.FloatField()
    timestamp=models.DateField(auto_now_add=True)


def __str__(self):
    return f"{self.temperatura}°C ({self.umidade}%)"    