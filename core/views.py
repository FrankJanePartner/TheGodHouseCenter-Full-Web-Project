from django.shortcuts import render
from .models import Leader, Location

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def belief(request):
    return render(request, 'our-beliefs.html')

def leaders(request):
    leader = Leader.objects.all()
    return render(request, 'leadership.html', {'leader':leader})

def locations(request):
    location = Location.objects.all()
    return render(request, 'location.html', {'location':location})