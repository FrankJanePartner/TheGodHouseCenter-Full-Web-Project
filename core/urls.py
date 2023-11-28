from django.urls import path, include
from .views import home, about, belief, leaders, locations, leaderdetails, locationdetails 

app_name='core'
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('belief/', belief, name='belief'),
    path('leaders/', leaders, name='leaders'),
    path('locations/', locations, name='locations'),
    path('leader/<slug:slug>', leaderdetails, name='leaderdetails'),
    path('location/<slug:slug>', locationdetails, name='locationdetails'),
]
