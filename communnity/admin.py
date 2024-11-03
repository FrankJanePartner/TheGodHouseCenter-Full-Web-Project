from django.contrib import admin
from .models import Unit, Church

# Register your models here.
class UnitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    
class ChurchAdmin(admin.ModelAdmin):
    prepopulated_field = {'slug': ('name',)}
    
admin.site.register(Unit, UnitAdmin)
admin.site.register(Church, ChurchAdmin)
