from django.urls import path
from .views import telainicial

app_name = "dashboard_frontend"

urlpatterns = [
    path('', telainicial, name='telainicial'),         
    path('inicio/', telainicial, name='inicio'),      
]
