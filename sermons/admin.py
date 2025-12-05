from django.contrib import admin
from .models import VideoMessage, AudioMessage

# Register your models here.
class VideoMessageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    
class AudioMessageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(VideoMessage, VideoMessageAdmin)
admin.site.register(AudioMessage, AudioMessageAdmin)
