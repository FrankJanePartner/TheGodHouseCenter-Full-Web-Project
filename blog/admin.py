from django.contrib import admin
from .models import Subscriber, Blog, BlogCategories

# Register your models here.
class BlogCategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(BlogCategories, BlogCategoriesAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Subscriber)
