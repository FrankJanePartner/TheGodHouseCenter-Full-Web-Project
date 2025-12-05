from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve
import os
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


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
    path('api/rvc/', include('runningWithTheVisionConference.urls', namespace='rvc')),
    path('wwc<int:pk>/', include('WholeWordConference.urls', namespace='wwc')),
    path('rezonance/', include('rezonance.urls', namespace='rezonance')),
    path('schoolofministry/', include('ministrySchool.urls', namespace='ministrySchool')),
    path('api/whole-word-tv/', include('WholeWordTv.urls', namespace='whole-word-tv')),
    
    #Favicon path
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),

    #third party app
    path('tinymce/', include('tinymce.urls')),
    # path("api/whole-word-tv/accounts/", include("allauth.urls")),
    # path("api/whole-word-tv/accounts/", include("dj_rest_auth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

