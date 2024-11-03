from django.shortcuts import render
from .models import Enquire, PrayerRequest, Testimony
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def contact(request):
    return render(request, 'contact.html')

def enquiry(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['message']
        enq = Enquire.objects.create(name=name, email=email, phone=phone_number, message=message)
    return render(request, 'enquiry.html')

def prayers(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['message']
        contactMe = request.POST.get('yes', False)
        DontContactMe = request.POST.get('no', False)
        
        should_contact = True if contactMe else False

        pryreq = PrayerRequest.objects.create(
            name=name, email=email, phone=phone_number, message=message, should_contact=should_contact
        )
        

    return render(request, 'prayer-request.html')
    
def testimony(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        testimony = request.POST.get('testimony')
        image = request.FILES.get('image')  # Use get() to safely access request.FILES

        if image is not None:
            testimony_obj = Testimony.objects.create(
                name=name, email=email, phone=phone_number, image=image, location=location, content=testimony
            )
        else:
            testimony_obj = Testimony.objects.create(
                name=name, email=email, phone=phone_number, location=location, content=testimony
            )

        # Send email notification
        subject = 'Alert!!! New Testimony'
        message = f"Testifier's name: {name}\nTestifier's Email: {email}\nTestifier's Phone: {phone_number}\nTestifier's Location: {location}\nTestifier's Testimony: {testimony}"
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = ['info@godhouse.org', 'apostletdphilips@gmail.com']
        #recipient_list = ['frankjanepartner@gmail.com', 'daminister14@gmail.com']
        send_mail(subject, message, sender_email, recipient_list, fail_silently=False)

        return render(request, 'testimony-success.html')

    return render(request, 'share-your-testimony.html')

    
