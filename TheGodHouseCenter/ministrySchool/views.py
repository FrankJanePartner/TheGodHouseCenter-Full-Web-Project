from django.shortcuts import render, redirect
from core.models import Location
from .models import Attendee, FrontEndText
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging
from django.http import JsonResponse

# Create your views here.
def index(request):
    attendee = Attendee.objects.all()
    text = FrontEndText.objects.all()
    context = {
        'attendee':attendee,
        'text':text,
    }
    return render(request, 'ministrySchool/school_of_ministry.html', context)

def attendee(request):

    attendee = Attendee.objects.all()

    context = {
        'attendee':attendee,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        how_will_you_attend = request.POST.get('attending')
        email = request.POST.get('email')
        image = request.FILES.get('image')

        Attendee.objects.create(
            name=name,
            phone=phone,
            how_will_you_attend=how_will_you_attend,
            email=email,
            proof_of_payment=image,
        )
        
        # Prepare email notification
        subject = 'Alert!!! New Registration'
        message = (
            f"Student's Name: {name}\n"
            f"Student's Email: {email}\n"
            f"Student's Phone: {phone}\n"
            f"Student will be attending: {how_will_you_attend}\n"
        )
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = ['apostletdphilips@gmail.com', 'schoolofministry@godhouse.org', 'pastortony@godhouse.org']

        # Use EmailMessage for email with optional attachment
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=sender_email,
            to=recipient_list,
        )
        
        # Attach the image if it exists
        if image:
            email_message.attach(image.name, image.read(), image.content_type)

        # Send the email
        email_message.send(fail_silently=False)

        
        return render(request, 'ministrySchool/schoolSuccess.html')
        
