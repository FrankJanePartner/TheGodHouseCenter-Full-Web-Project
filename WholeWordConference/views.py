from django.shortcuts import render, redirect
from core.models import Location
from .models import Attendee, FieldModel
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request):
    attendee = Attendee.objects.all()
    locations = Location.objects.all()
    files = FieldModel.objects.all()
    context = {
        'attendee':attendee,
        'locations':locations,
        "files":files
    }
    return render(request, 'wwc.html', context)

def attendee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        ministry = request.POST.get('ministry')
        ministry_status = request.POST.get('ministry-status')
        how_did_you_know = request.POST.get('know')
        how_will_you_attend = request.POST.get('attending')
        email = request.POST.get('email')
        godhouse_location = request.POST.get('godhouse-location')
        need_accommodation = request.POST.get('need')

        Attendee.objects.create(
            name=name,
            phone=phone,
            ministry=ministry,
            ministry_status=ministry_status,
            how_did_you_know=how_did_you_know,
            how_will_you_attend=how_will_you_attend,
            email=email,
            godhouse_location=godhouse_location,
            need_accommodation=need_accommodation
        )
        return render(request, 'success.html')
    #return redirect("reverse('wwc.html')")
        