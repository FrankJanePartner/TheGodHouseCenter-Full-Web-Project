from django.urls import path
from .views import rezonanceMain, videoStream, download

app_name = 'rezonance'

urlpatterns = [
    path('', rezonanceMain, name='rezonanceMain'),
    path('videoStream/<slug:slug>', videoStream, name='videoStream'),
    path('download/<int:id>/', download, name='download'),
]