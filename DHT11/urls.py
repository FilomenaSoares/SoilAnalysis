from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DHT11ViewSet

router = DefaultRouter()
router.register(r'dados', DHT11ViewSet, basename='dht11')

urlpatterns = router.urls  
