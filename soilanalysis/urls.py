from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter

from DHT11.views import DHT11ViewSet
from sensorumidade.views import sensorumidadeViewSet
from dashboard_frontend import views as dashboard_views

router = DefaultRouter()
router.register(r'dados/dht11', DHT11ViewSet, basename='dht11')
router.register(r'dados/umidade', sensorumidadeViewSet, basename='umidade')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('dashboard_frontend/', include('dashboard_frontend.urls', namespace='dashboard_frontend')),
    
    path('', lambda request: redirect('dashboard_frontend:telainicial')),

    path('umidade-solo/gerenciar/', dashboard_views.gerenciar_umidade_solo, name='gerenciar_umidade_solo'),


]