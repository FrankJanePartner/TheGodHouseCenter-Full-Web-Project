from django.shortcuts import render
from .models import Blog
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def home(request):
    post = Blog.objects.all()
    context = {
        "post":post
    }
    return render(request, 'blogs.html', context)

def allPost(request):
    blog = Blog.objects.all()
    context = {
        "blog":blog
    }
    return render(request, 'all-post.html', context)

def details(request):
    blog = Blog.objects.all()
    context = {
        "blog":blog
    }
    return render(request, 'post.html', context)
