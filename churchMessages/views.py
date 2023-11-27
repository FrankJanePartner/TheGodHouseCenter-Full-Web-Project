from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request, 'sermon.html', context)

def videoStream(request, slug):
    # get all the videos and audio form the database
    video = VideoMessage.objects.all()
    product = get_object_or_404(AudioMessage, slug=slug)
    context = {
        'video': video
    }
    return render(request, 'audioStream.html', context)

def audioStream(request, slug):
    # get all the videos and audio form the database
    product = get_object_or_404(AudioMessage, slug=slug)

    audio = AudioMessage.objects.all()
    context = {
        'audio': audio,
    }
    return render(request, 'videoStream.html', context)

# download youtube video using video embed id
def downloadVideo(request, slug):
    if request.method == "POST":
        video = get_object_or_404(VideoMessage, slug=slug)
        print("downloading")
        url = f"https://www.youtube.com/watch?v={video.embed}"
        response = requests.get(url, stream=True)
        