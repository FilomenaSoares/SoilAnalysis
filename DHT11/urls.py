from django.urls import path
from .views import dht11_frontend
from rest_framework.routers import DefaultRouter
from .views import DHT11ViewSet

router = DefaultRouter()
router.register(r'dados', DHT11ViewSet, basename='dht11')

urlpatterns = [
    path('frontend/', dht11_frontend, name='dht11_frontend'),
]

urlpatterns += router.urls
