from django.urls import path
from . import views

urlpatterns = [
    path('', views.routePlanner, name='route-planner'),
    path('test/', views.getRoutes, name='test'),
    path('view/', views.showRoute, name='view-route'),
]
