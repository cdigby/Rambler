from django.urls import path
from . import views

urlpatterns = [
    path('', views.routePlanner(), name='route-planner'),

]
