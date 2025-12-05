from django.shortcuts import render, redirect, get_object_or_404
from core.models import Location
from .models import Attendee, SlideImage, WholeWordConference, Schedule
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request, pk):
    wy = f'wwc{pk}'
    wwc = get_object_or_404(WholeWordConference, slug=wy)
    locations = Location.objects.all()
    files = SlideImage.objects.all()
    sessions = Schedule.objects.all()
    context = {
        'wwc':wwc,
        "files":files,
        'locations':locations,
        'sessions':sessions
    }
    
    return render(request, 'wwc/wwc.html', context)
    