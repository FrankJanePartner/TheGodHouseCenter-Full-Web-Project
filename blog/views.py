from django.shortcuts import render
from .models import Blog, BlogCategories
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def home(request):
    post = Blog.objects.all()
    category = BlogCategories.objects.all()
    context = {
        "post":post,
        "category":category
    }
    return render(request, 'home.html', context)

def allPost(request):
    post = Blog.objects.all()
    category = BlogCategories.objects.all()
    context = {
        "post":post,
        "category":category
    }
    return render(request, 'all-post.html', context)

def details(request):
    post = Blog.objects.all()
    category = BlogCategories.objects.all()
    context = {
        "post":post,
        "category":category
    }
    return render(request, 'post.html', context)
