from django.shortcuts import render
from .models import Subscriber, Blog, Category
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Subscriber

# Create your views here.
def home(request):
    post = Blog.objects.all()
    category = Category.objects.all()
    context = {
        "post":post,
        "category":category
    }
    return render(request, 'home.html', context)

def allPost(request):
    post = Blog.objects.all()
    category = Category.objects.all()
    context = {
        "post":post,
        "category":category
    }
    return render(request, 'all-post.html', context)

def details(request):
    post = Blog.objects.all()
    category = Category.objects.all()
    context = {
        "post":post,
        "category":category
    }
    return render(request, 'post.html', context)

def subscriber(request):
    if request.method == 'POST':
        email = request.POST['email']
        new_subscriber = Subscriber(user=email)
        new_subscriber.save()

        subject = 'New Subscriber'
        message = f'A new subscriber has signed up with the email: {email}'
        from_email = 'partnermarvel55@gmail.com'
        recipient_list = ['partnermarvel55@gmail.com']
        send_mail(subject, message, from_email, recipient_list)

        return redirect('success_page')
    else:
        return HttpResponse('Invalid request')
