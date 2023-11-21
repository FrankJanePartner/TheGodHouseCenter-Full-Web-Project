from django.urls import path
from .views import churches, units

app_name = 'community'
urlpatterns = [
    path('', churches, name='churches'),
    path('', units, name='units'),
]
