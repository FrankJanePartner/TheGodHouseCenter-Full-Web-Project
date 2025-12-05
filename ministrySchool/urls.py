from django.urls import path
from .views import index, attendee

app_name = "ministrySchool/"

urlpatterns = [
    path("", index, name='index'),
    path("register/", attendee, name='register')
]

