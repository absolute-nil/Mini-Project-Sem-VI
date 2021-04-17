from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tester',views.tester,name='tester'),
    path('video_feed', views.video_feed, name='video_feed'),
]