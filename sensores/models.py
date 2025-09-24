from django.db import models

class sensor (models.Model):

 name_sensor=models.CharField(max_length=30)
 localization=models.CharField(max_length=40, blank=True)
 criado_dia=models.DateField(auto_now_add=True)

def __str__(self):
    return f"{self.name} ({self.location})"

class DHT11Data (models.Model):
  
  sensor=models.ForeignKey(sensor, on_delete=models.CASCADE)
  temperatura=models.FloatField()
  umidade=models.FloatField()
  timestamp=models.DateField(auto_now_add=True)

def __str__(self):
    return f"{self.name} ({self.location})"  