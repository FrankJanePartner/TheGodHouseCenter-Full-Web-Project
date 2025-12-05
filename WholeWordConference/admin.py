from django.contrib import admin
from .models import Attendee, SlideImage, WholeWordConference, Schedule
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages


  
@admin.action(description="Export selected attendees as CSV")
def export_as_csv(Attendee, request, queryset):  # ✅ Correct number of arguments
    model = Attendee.model
    meta = model._meta
    fieldnames = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}.csv'

    writer = csv.writer(response)
    writer.writerow(fieldnames)

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fieldnames])

    return response

    
    
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    
    
    
class SlideImageInline(admin.TabularInline):
    model = SlideImage
    extra = 1
    


class AttendeeAdmin(admin.ModelAdmin):
    list_filter = [("whole_word_conference", admin.RelatedOnlyFieldListFilter)]
    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        # Check if filter is applied
        if 'whole_word_conference__id__exact' not in request.GET:
            current_year = timezone.now().year
            try:
                wwc = WholeWordConference.objects.get(date__year=current_year)
                q = request.GET.copy()
                q['whole_word_conference__id__exact'] = str(wwc.id)
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()
                
            except WholeWordConference.DoesNotExist:
                messages.info(request, f"Attendees data for this year does not exit.")

        return super().changelist_view(request, extra_context=extra_context)



class WholeWordConferenceAdmin(admin.ModelAdmin):
    inlines = [
        SlideImageInline,
        ScheduleInline
    ]
    
admin.site.register(WholeWordConference,  WholeWordConferenceAdmin)
admin.site.register(Attendee, AttendeeAdmin)

