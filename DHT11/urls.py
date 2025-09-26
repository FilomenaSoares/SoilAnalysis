from rest_framework.routers import DefaultRouter
from .views import DHT11ViewSet

router = DefaultRouter()
router.register(r'dht11', DHT11ViewSet, basename='dht11')

urlpatterns = router.urls