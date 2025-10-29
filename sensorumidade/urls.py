from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import sensorumidadeViewSet

router = DefaultRouter()
router.register(r'dados', sensorumidadeViewSet, basename='umidadesolo')



urlpatterns = router.urls
