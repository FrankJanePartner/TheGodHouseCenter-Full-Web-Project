from django.shortcuts import render, redirect
from .models import Enquire, PrayerRequest, Testimony
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging
from django.http import JsonResponse


# Create your views here.
def contact(request):
    return render(request, 'contact/contact.html')

def enquiry(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            message = request.POST['message']
            
            if not name or not message:
                return JsonResponse({"error": "Name and message are required fields."}, status=400)
            
            enq = Enquire.objects.create(name=name, email=email, phone=phone_number, message=message)
            
            
            subject = 'Alert!!! New Enquiry'
            message = f"Requester's name: {name}\nRequester's Email: {email}\nRequester's Phone: {phone_number}\nRequester's Prayer Request: {message}."
            sender_email = settings.EMAIL_HOST_USER
            recipient_list = ['info.godhouse@gmail.com', 'apostletdphilips@gmail.com']
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False)
            
            # Return success response
            return JsonResponse({"success": True, "message": "Enquiry submitted successfully!"})

        except Exception as e:
            # Log the exception (optional, ensure logger is configured)
            return JsonResponse({"error": "An error occurred. Please try again later."}, status=500)
    return render(request, 'contact/enquiry.html')

def prayers(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['message']
        contactMe = request.POST.get('yes', False)
        DontContactMe = request.POST.get('no', False)
        
        should_contact = True if contactMe else False
        
        if not name or not phone_number or not message:
            return JsonResponse({"error": "Please fill in all required fields."}, status=400)


        pryreq = PrayerRequest.objects.create(
            name=name, email=email, phone=phone_number, message=message, should_contact=should_contact
        )
        
        # Send email notification
        if should_contact == True:
            subject = 'Alert!!! New Prayer Request'
            message = f"Requester's name: {name}\nRequester's Email: {email}\nRequester's Phone: {phone_number}\nRequester's Prayer Request: {message}. Please contact me"
            sender_email = settings.EMAIL_HOST_USER
            recipient_list = ['info@godhouse.org', 'apostletdphilips@gmail.com']
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False)
            
            return JsonResponse({"success": True, "message": "Prayer request submitted successfully!"})
        elif should_contact == False:
            subject = 'Alert!!! New Prayer Request'
            message = f"Requester's name: {name}\nRequester's Email: {email}\nRequester's Phone: {phone_number}\nRequester's Prayer Request: {message}. Please don't contact"
            sender_email = settings.EMAIL_HOST_USER
            recipient_list = ['info.godhouse@gmail.com', 'apostletdphilips@gmail.com']
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False)
            
            return JsonResponse({"success": True, "message": "Prayer request submitted successfully!"})
    return render(request, 'contact/prayer-request.html', )
    
def testimony(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        testimony_content = request.POST.get('testimony')
        image = request.FILES.get('image')  # Use get() to safely access request.FILES
        
         # Validate required fields
        if not name or not testimony_content:
            return JsonResponse({"error": "Name and testimony content are required."}, status=400)

        # Create Testimony object
        testimony_obj = Testimony.objects.create(
            name=name,
            email=email,
            phone=phone_number,
            location=location,
            content=testimony_content,
            image=image if image else None,
        )

        # Prepare email notification
        subject = 'Alert!!! New Testimony'
        message = (
            f"Testifier's Name: {name}\n"
            f"Testifier's Email: {email}\n"
            f"Testifier's Phone: {phone_number}\n"
            f"Testifier's Location: {location}\n"
            f"Testifier's Testimony: {testimony_content}"
        )
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = ['info.godhouse@gmail.com', 'apostletdphilips@gmail.com']

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

        return JsonResponse({"message": "Testimony submitted successfully!"})
    return render(request, 'contact/share-your-testimony.html')


def testimonySuccess(request):
    return render(request, "contact/testimony-success.html")
