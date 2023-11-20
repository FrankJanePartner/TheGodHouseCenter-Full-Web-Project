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

def download(request):
    # get the video or audio selected and download it to the users device
    if request.method == "POST":
        id = int(request.POST['id'])
        type = str(request.POST['type'])
        if type == 'Video':
            obj = get_object_or_404(VideoMessage, pk=id)
            filepath = obj.file.url
        elif type == 'Audio':
            obj = get_object_or_404(AudioMessage, pk=id)
            filepath = obj.file.url
        else:
            print('Invalid Type')
        return redirect('/message/')