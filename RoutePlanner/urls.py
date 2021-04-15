from django.urls import path
from . import views

urlpatterns = [
    path('planner/', views.routePlanner, name='route-planner'),
    path('test/', views.getRoutes, name='test'),
]
