from django.shortcuts import render, get_object_or_404
from .models import Album, SocailMedia, Video, LifePerformance, LifePerformanceImage
from django.http import FileResponse

# Create your views here.
def rezonanceMain(request):
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
    return render(request, 'rezonance/resonance.html', context)
    
    
def videoStream(request, slug):
    video = get_object_or_404(Video, slug=slug)
    
    context = {
        "video": video,
    }
    return render(request, 'rezonance/lyrics.html', context)




def download(request, id):
    file = get_object_or_404(Video, id=id)
    response = FileResponse(file.audioFile.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{file.audioFile.name.split("/")[-1]}"'
    return response


