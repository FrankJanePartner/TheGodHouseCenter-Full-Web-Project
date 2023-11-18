from django.shortcuts import render

# Create your views here.
def testimony(request):
    return render(request, 'testimony.html')

def details(request):
    return render(request, 'testimony-details.html')

def image(request):
    return render(request, 'testimony-image.html')
