from django.contrib import admin
from .models import sensor, DHT11Data

admin.site.register(sensor)
admin.site.register(DHT11Data)
