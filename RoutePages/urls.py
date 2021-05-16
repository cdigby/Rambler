from django.urls import path
from . import views

app_name = 'RoutePages'
urlpatterns = [
    path('<int:id>/', views.displayRoutePage, name='route-page'),
]