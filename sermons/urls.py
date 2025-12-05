from django.urls import path
from .views import message, sermon_detail, videoStream

app_name = "sermons"
urlpatterns = [
    path('', message, name='message'),
    path('item/<slug:slug>', sermon_detail, name='sermon_detail'),
    path('video/<slug:slug>', videoStream, name='videoStream'),
]
