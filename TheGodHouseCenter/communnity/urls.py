from django.urls import path
from .views import units, churches

app_name = 'community'
urlpatterns = [
    path('<slug:slug>/', churches, name='churches'),
    path('unit', units, name='units'),
]