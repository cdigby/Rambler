from django.urls import path
from . import views

app_name = 'RoutePlanner'
urlpatterns = [
    path('', views.routePlanner, name='route-planner'),
    path('test/', views.getRoutes, name='test'),
    path('view/', views.showRoute, name='view-route'),
]
