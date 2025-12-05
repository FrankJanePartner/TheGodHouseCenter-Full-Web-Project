from django.urls import path
from .views import testimony, details

app_name = 'testimony'
urlpatterns = [
    path('', testimony, name='testimony'),
    path('details/<slug:slug>', details, name='details'),
]
