from django.urls import path
from .views import testimonyImage, testimony, details

urlpatterns = [
    path('', testimony, name='testimony'),
    path('testimonyImage', testimonyImage, name='testimonyImage'),
    path('details/', details, name='details'),
]
