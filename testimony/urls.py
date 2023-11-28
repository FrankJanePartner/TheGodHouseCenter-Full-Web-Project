from django.urls import path
from .views import testimonyImage, testimony, details

app_name = 'testimony'
urlpatterns = [
    path('', testimony, name='testimony'),
    path('testimonyImage', testimonyImage, name='testimonyImage'),
    path('details/<slug:slug>', details, name='details'),
]
