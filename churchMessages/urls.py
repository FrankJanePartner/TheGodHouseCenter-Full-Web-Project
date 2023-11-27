from django.urls import path
from .views import message, download, videoStream, audioStream

urlpatterns = [
    path('', message, name='message'),
    path('videoStream/', videoStream, name='videoStream'),
    path('audioStream/', audioStream, name='audioStream'),
    path('download/', download, name='download'),
]
