from django.contrib import admin
from .models import Attendee, FrontEndText
from django.http import HttpResponse
import csv

class AttendeeAdmin(admin.ModelAdmin):
    model = Attendee
    fields = ['name','email', 'phone', 'how_will_you_attend', 'proof_of_payment']
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
    
    export_as_csv.short_description = 'Export selected attendees as CSV'

admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(FrontEndText)
