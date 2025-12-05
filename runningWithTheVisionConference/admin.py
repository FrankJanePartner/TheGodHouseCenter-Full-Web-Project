from django.contrib import admin
from .models import Registration, Moment
from django.http import HttpResponse
import csv

class RegistrationAdmin(admin.ModelAdmin):
    model = Registration
    fields = ["firstName", "lastName", "email", "phone", "city", "churchType", "godhouseCentre", "otherChurch", "attendanceType", "accommodation"]

    actions = ['export_as_csv']
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        
        writer = csv.writer(response)
        writer.writerow(fieldnames)
        
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in fieldnames])
            
        return response
    
    export_as_csv.short_description = 'Export selected Registrations as CSV'

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Moment)
