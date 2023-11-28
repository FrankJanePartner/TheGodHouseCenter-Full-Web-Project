from django.urls import path
from .views import message, downloadVideo, videoStream, audioStream

app_name = "sermons"
urlpatterns = [
    path('', message, name='message'),
    path('videoStream/<slug:slug>', videoStream, name='videoStream'),
    path('audioStream/<slug:slug>', audioStream, name='audioStream'),
    path('downloadVideo/', downloadVideo, name='downloadVideo'),
]
