from django.urls import path, include
from . import views

app_name = 'Weather'
urlpatterns = [
    path('', views.weather, name='weather-page'),
]