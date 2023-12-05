from django.shortcuts import render
from .models import Enquire, PrayerRequest

# Create your views here.
def contact(request):
    return render(request, 'contact.html')

def enquiry(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['message']
        enq = Enquire.objects.create(name=name, email=email, tel=phone_number, message=message)
    return render(request, 'enquiry.html')

def prayers(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['message']
        contactMe = request.POST['yes']
        DontContactMe = request.POST['no']
        if contactMe.value == True:
            pryreq = PrayerRequest.objects.create(name=name, email=email, tel=phone_number, message=message, should_contact=True) 
        elif DontContactMe.value == True:
            pryreq = PrayerRequest.objects.create(name=name, email=email, tel=phone_number, message=message, should_contact=False)
    return render(request, 'prayer-request.html')
