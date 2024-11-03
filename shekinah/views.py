from django.shortcuts import render
from .models import Album, SocailMedia, Video, LifePerformance, LifePerformanceImage

# Create your views here.
def shekinah(request):
    album = Album.objects.all()
    socailMedia = SocailMedia.objects.all()
    video = Video.objects.all()
    lifePerformance = LifePerformance.objects.all()
    
    context = {
        "album": album,
        "socailMedia": socailMedia,
        "video": video,
        "lifePerformance": lifePerformance,
    }
    return render(request, 'shekinah.html', context)
