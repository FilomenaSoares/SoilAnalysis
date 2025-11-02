from django.db import models
from django.utils import timezone

class sensorumidadeData(models.Model):
    umidadesolo = models.FloatField()
    timestampSolo = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        if isinstance(self.timestampSolo, timezone.datetime):
             return f"{self.timestampSolo.strftime('%Y-%m-%d %H:%M')} - {self.umidadesolo}%"
