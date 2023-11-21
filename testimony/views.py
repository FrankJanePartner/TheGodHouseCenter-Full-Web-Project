from django.shortcuts import render
from .models import Testimony, TestimonyImage
# Create your views here.

def testimony(request):
    testimony = Testimony.objects.all()
    return render(request, 'testimony.html', {'testimony':testimony})

def details(request):
    return render(request, 'testimony-details.html')

def testimonyImage(request):
    testimg = TestimonyImage.objects.all()
    return render(request, 'testimony.html', {'testimg':testimg})

#create a function that ensures only a max of 9 instance of the TestimonyImage can exist. i.e oldest instance is deleted to create a new instance once the total instance is greater than 9