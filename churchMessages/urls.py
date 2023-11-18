from django.urls import path
from . import views

urlpatterns = [
    path('', views.message, name='message'),
    path('audio/', views.audioMessages, name='audio'),
    path('video/', views.videoMessages, name='video')
]
