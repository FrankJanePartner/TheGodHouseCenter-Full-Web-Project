from django.shortcuts import render, get_object_or_404, redirect
from .models import Leader, Location, ServiceDay, LeaderSocialMedia
from communnity.models import Unit
from WholeWordConference.models import Attendee, WholeWordConference
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
import logging
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.generic import TemplateView

# Create your views here.
def home(request):
    units = Unit.objects.all()
    context = {
        'units':units
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def belief(request):
    return render(request, 'core/our-beliefs.html')
    

def wholewordtv(request):
    return render(request, 'core/channel.html')
    
#class WholeWordTVFrontendView(TemplateView):
#    template_name = 'wholewordtv/index.html'

def leaders(request):
    leader = Leader.objects.all()
    return render(request, 'core/leadership.html', {'leader':leader})

def locations(request):
    location = Location.objects.all()
    return render(request, 'core/location.html', {'location':location})

def leaderdetails(request, slug):
    # get the leader and associated social media profiles from the database
    leader = get_object_or_404(Leader, slug=slug)
    socialMedia = leader.leadersocialmedias.all()

    context = {
        'leader': leader,
        'socialMedia': socialMedia,
    }
    return render(request, 'core/papa.html', context)

def locationdetails(request, slug):
    # get all the videos and audio form the database
    location = get_object_or_404(Location, slug=slug)
    service = location.service_days.all()
    context = {
        'location': location,
        'service': service,
    }
    return render(request, 'core/location1.html', context)
    
def wwc_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        phone = request.POST.get('phone')
        ministry = request.POST.get('ministry')
        ministry_status = request.POST.get('ministry-status')
        how_did_you_know = request.POST.get('know')
        how_will_you_attend = request.POST.get('attending')
        email = request.POST.get('email')
        godhouse_location = request.POST.get('godhouse-location')
        need_accommodation = request.POST.get('need')
        
        today = datetime.today().date()
        year = today.year
        
        email_message = WholeWordConference.objects.get(date__year=year)
        try:
            sendmessage = email_message.email_message
        except WholeWordConference.DoesNotExist:
            sendmessage = "Thank you for registering."

        Attendee.objects.create(
            whole_word_conference=email_message,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            ministry=ministry,
            ministry_status=ministry_status,
            how_did_you_know=how_did_you_know,
            how_will_you_attend=how_will_you_attend,
            email=email,
            godhouse_location=godhouse_location,
            need_accommodation=need_accommodation
        )

        subject = 'Thank You for Registering!'
        message = sendmessage
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        html_content = message  # HTML from TinyMCE
        text_content = strip_tags(message)  # Strips HTML tags for plain text fallback
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=sender_email,
            to=recipient_list,
        )
        email.attach_alternative(html_content, "text/html")  # Attach HTML version
        email.send(fail_silently=False)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            success_url = reverse('core:success')  # Make sure this is your success URL name
            return JsonResponse({'redirect_url': success_url}, status=200)

        return redirect('core:success')  # Fallback if not AJAX

    return JsonResponse({'error': 'Invalid method'}, status=400)
    
def success(request):
    return render(request, 'wwc/success.html')

