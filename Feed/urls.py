from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views



app_name= "Feed"

urlpatterns=[
    path('', views.display_feed, name='feed')
]