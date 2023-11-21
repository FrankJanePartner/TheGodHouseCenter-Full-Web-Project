from django.urls import path
from .views import message, download

urlpatterns = [
    path('', message, name='message'),
    path('download/', download, name='download'),
]
