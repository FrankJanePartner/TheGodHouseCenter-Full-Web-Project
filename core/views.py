from django.shortcuts import render,  get_object_or_404
from .models import Leader, Location, ServiceDay, HeaderInfo, LeaderSocialMedia
from communnity.models import Unit, Church
#from blog.models import Blog
#from testimony.models import Testimony

# Create your views here.
def home(request):
    units = Unit.objects.all()
    churches = Church.objects.all()
    #blog = Blog.objects.all()
   # testimony = Testimony.objects.all()
    header = HeaderInfo.objects.all()
    context = {
        #'blog':blog,
        'units':units,
        'churches':churches,
        #'testimony':testimony,
        'header':header
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def belief(request):
    return render(request, 'our-beliefs.html')
    
def wholewordtv(request):
    return render(request, 'channel.html')

def leaders(request):
    leader = Leader.objects.all()
    return render(request, 'leadership.html', {'leader':leader})

def locations(request):
    location = Location.objects.all()
    return render(request, 'location.html', {'location':location})

def leaderdetails(request, slug):
    # get the leader and associated social media profiles from the database
    leader = get_object_or_404(Leader, slug=slug)
    socialMedia = leader.leadersocialmedias.all()

    context = {
        'leader': leader,
        'socialMedia': socialMedia,
    }
    return render(request, 'papa.html', context)

def locationdetails(request, slug):
    # get all the videos and audio form the database
    location = get_object_or_404(Location, slug=slug)
    service = location.service_days.all()
    context = {
        'location': location,
        'service': service,
    }
    return render(request, 'location1.html', context)