from django.urls import path
from .views import shekinah

app_name = 'shekinah'

urlpatterns = [
    path('', shekinah, name='shekinah'),
]