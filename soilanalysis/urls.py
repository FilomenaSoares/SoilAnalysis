from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from DHT11.views import DHT11ViewSet

# Configurações do DRF
router = DefaultRouter()
router.register(r'dados', DHT11ViewSet, basename='dht11')

urlpatterns = [
    path('api/', include(router.urls)),          # API JSON
    path('dht11/', include('DHT11.urls')),      # Frontend do DHT11
    path('', lambda request: redirect('dht11/frontend/')),  # Raiz redireciona para frontend
]
