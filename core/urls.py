from django.urls import path, include
from .views import home, about, belief, wholewordtv, leaders, locations, leaderdetails, locationdetails, wwc_register, success
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve  # ✅ this line fixes the error
import os
from django.conf import settings
from django.conf.urls.static import static
from legal.views import privacy,  terms



app_name='core'

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('belief/', belief, name='belief'),
    path('leaders/', leaders, name='leaders'),
    path('locations/', locations, name='locations'),
    path('leader/<slug:slug>', leaderdetails, name='leaderdetails'),
    path('location/<slug:slug>', locationdetails, name='locationdetails'),
    path('register/', wwc_register, name='register'),
    path('success/',success, name='success'),
    path('terms/', terms, name="terms"),
    path('privacy/', privacy, name="privacy"),

   # path('<slug:slug>', include('WholeWordConference.urls', namespace='wwc')),
]
