from django.contrib import admin
from .models import PrayerRequest, Enquire, Testimony

# Register your models here.
admin.site.register(Enquire)
admin.site.register(PrayerRequest)
admin.site.register(Testimony)