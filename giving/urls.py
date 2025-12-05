from django.urls import path
from .views import giving

urlpatterns = [
    path('', giving, name='giving'),
]