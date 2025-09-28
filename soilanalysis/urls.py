from django.urls import path, include
from rest_framework.routers import DefaultRouter
from DHT11.views import dht11_frontend, DHT11ViewSet

router = DefaultRouter()
router.register(r'dados', DHT11ViewSet, basename='dht11')

urlpatterns = [
    path('api/', include(router.urls)),    #api para jason
    path('dht11/', include('DHT11.urls')),  #frontend - 8000/dht11/frontend/
]
from django.urls import path, include


