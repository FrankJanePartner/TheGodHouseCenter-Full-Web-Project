from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
from .models import VideoMessage, AudioMessage

# Create your views here.
def message(request):
    # get all the videos and audio form the database
    # get the use selected video or audio
    # display the video to the frontend

    return render(request, 'sermon.html')

def download(request):
    # save the file of the user selected video
    pass

def videoMessages(request):
    videoMessages = VideoMessage.objects.all()
    context={
        'videoMessages':videoMessages
    }
    return render(request, 'videoStream.html', context)

def audioMessages(request):
    audioMessages = AudioMessage.objects.all()
    context={
        'audioMessages':audioMessages
    }
    return render(request, 'audioStream.html', context)