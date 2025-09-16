from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Leader, Location, Category, ServiceDay, LeaderSocialMedia, HeaderInfo
from django.http import HttpResponse
import csv

# Register your models here.

admin.site.unregister(Group)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(HeaderInfo)
admin.site.register(ServiceDay)
admin.site.register(Leader)
admin.site.register(LeaderSocialMedia)

