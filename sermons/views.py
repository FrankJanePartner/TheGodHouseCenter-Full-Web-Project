from django.shortcuts import render, get_object_or_404
# from django.contrib import messages
from .models import VideoMessage, AudioMessage

# Create your views here.
def message(request):
    # get all the videos and audio form the database
    video = VideoMessage.objects.all()
    audio = AudioMessage.objects.all()
    context = {
        'video': video,
        'audio': audio,
    }
    return render(request, 'revised.html', context)
    
def sermon_detail(request, slug):
    audio = get_object_or_404(AudioMessage, slug=slug)
    return render(request, 'sermonDetail.html', {'audio': audio})
    
def videoStream(request, slug):
    video = get_object_or_404(VideoMessage, slug=slug)
    return render(request, 'videoStream.html', {'video': video})
