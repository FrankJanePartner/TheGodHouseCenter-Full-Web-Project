from django.urls import path, include
from .views import home, about, belief, leaders, locations

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('belief/', belief, name='belief'),
    path('leaders/', leaders, name='leaders'),
    path('locations/', locations, name='locations')
]
