from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def belief(request):
    return render(request, 'our-beliefs.html')

def leaders(request):
    return render(request, 'leadership.html')

def locations(request):
    return render(request, 'location.html')