"""
URL configuration for TheGodhouseCenter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'The Godhouse Center'
admin.site.site_title = 'The Godhouse center Admin Panel'
admin.site.index_title = 'Godhouse Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('basket/', include('basket.urls')),
    path('blog/', include('blog.urls')),
    path('churchMessages/', include('churchMessages.urls', namespace='sermons')),
    path('community/', include('communnity.urls', namespace='community')),
    path('contact/', include('contact.urls')),
    path('events/', include('events.urls')),
    path('give/', include('giving.urls')),
    path('store/', include('store.urls', namespace='store')),
    path('testimony/', include('testimony.urls', namespace='testimony')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)