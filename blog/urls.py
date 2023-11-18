from django.urls import path
from .views import home, allPost, details, contact, carrier

app_name = 'blog'
urlpatterns = [
    path('', home, name='home'),
    path('allPost/', allPost, name='allPost'),
    path('details/', details, name='details'),
    path('contact/', contact, name='contact'),
    path('carrier/', carrier, name='carrier'),
]
