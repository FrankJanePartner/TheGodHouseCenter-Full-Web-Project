from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Leader, Location, Category

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(Location)
admin.site.register(Leader)
admin.site.register(Category)