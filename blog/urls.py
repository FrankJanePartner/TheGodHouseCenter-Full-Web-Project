from django.urls import path
from .views import home, allPost, details

app_name = 'blog'
urlpatterns = [
    path('', home, name='home'),
    path('allPost/', allPost, name='allPost'),
    path('details/', details, name='details'),
]
