from django.shortcuts import render, get_object_or_404
from .models import Testimony, TestimonyImage
# Create your views here.

def testimony(request):
    testimony = Testimony.objects.all()
    testimg = TestimonyImage.objects.all()
    context = {
        'testimony':testimony,
        'testimg':testimg
    }
    return render(request, 'testimony.html', context)

def details(request, slug):
    testimony = get_object_or_404(Testimony, slug=slug)
    return render(request, 'testimony-details.html', {'testimony':testimony})

