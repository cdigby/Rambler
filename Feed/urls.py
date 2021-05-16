from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views
from RoutePages import views as RoutePageViews



app_name= "Feed"

urlpatterns=[
    path('', views.display_feed, name='feed'),
]