from django.urls import path, include
from .views import Events

urlpatterns = [
    path('', Events, name='events'),
]