from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'The Godhouse Center'
admin.site.site_title = 'The Godhouse center Admin Panel'
admin.site.index_title = 'Godhouse Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #my app url
    path('', include('core.urls', namespace='core')),
    path('churchMessages/', include('sermons.urls', namespace='sermons')),
    path('community/', include('communnity.urls', namespace='community')),
    path('contact/', include('contact.urls')),
    path('events/', include('events.urls')),
    path('give/', include('giving.urls')),
    path('store/', include('store.urls', namespace='store')),
    path('testimony/', include('praiseReport.urls', namespace='testimony')),
    path('wwc2024/', include('WholeWordConference.urls', namespace='wwc2024')),
    path('shekinah/', include('shekinah.urls', namespace='shekinah')),
    path('rvc2024/', include('runningWithTheVisionConference.urls', namespace='rvc2024')),

    #third party app
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
