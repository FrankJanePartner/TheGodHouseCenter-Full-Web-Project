from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Album, SocailMedia, Video, LifePerformance, LifePerformanceImage
from django import forms

# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class SocailMediaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class LifePerformanceImageInline(admin.TabularInline):
    model = LifePerformanceImage

class LifePerformanceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        LifePerformanceImageInline
    ]

admin.site.register(Album, AlbumAdmin)
admin.site.register(SocailMedia, SocailMediaAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(LifePerformance, LifePerformanceAdmin)
