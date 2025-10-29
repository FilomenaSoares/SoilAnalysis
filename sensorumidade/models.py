from django.db import models

class sensorumidadeData(models.Model):
    umidadesolo=models.FloatField()
    timestampSolo = models.FloatField()


    def __str__(self):
        return f"Sensor {self.sensor_id} - {self.umidadesolo}%" 