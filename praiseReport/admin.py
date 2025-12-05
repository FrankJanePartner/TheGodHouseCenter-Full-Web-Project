from django.contrib import admin
from .models import Testimony, TestimonyImage

class TestimonyAdmin(admin.ModelAdmin):
    list_display = ['Testifer_names', 'content']
    prepopulated_fields = {'slug': ('Testifer_names',)}

admin.site.register(Testimony, TestimonyAdmin)
admin.site.register(TestimonyImage)
