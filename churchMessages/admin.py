from django.contrib import admin
from .models import VideoMessage, AudioMessage

# Register your models here.
admin.site.register(VideoMessage)
admin.site.register(AudioMessage)
