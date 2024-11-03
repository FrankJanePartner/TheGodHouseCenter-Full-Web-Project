from django.urls import path
from .views import index, attendee

app_name = "rvc2024/"

urlpatterns = [
    path("", index, name='index'),
    path("register/", attendee, name='register')
]

