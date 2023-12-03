from django.shortcuts import render,  get_object_or_404
from .models import Leader, Location, ServiceDay
from communnity.models import Unit, Church
from blog.models import Blog
from testimony.models import Testimony

# Create your views here.
def home(request):
    units = Unit.objects.all()
    churches = Church.objects.all()
    blog = Blog.objects.all()
    testimony = Testimony.objects.all()
    service = ServiceDay.objects.all()
    context = {
        'blog':blog,
        'units':units,
        'churches':churches,
        'testimony':testimony,
        'service': service
    }
    return render(request, 'home.html', context)

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

def leaderdetails(request, slug):
    # get all the videos and audio form the database
    audio = get_object_or_404(Leader, slug=slug)
    context = {
        'audio': audio,
    }
    return render(request, 'videoStream.html', context)

def locationdetails(request, slug):
    # get all the videos and audio form the database
    location = get_object_or_404(Location, slug=slug)
    context = {
        'location': location,
    }
    return render(request, 'location1.html', context)