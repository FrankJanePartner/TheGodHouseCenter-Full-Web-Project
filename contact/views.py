from django.shortcuts import render

# Create your views here.
def contact(request):
    return render(request, 'contact.html')

def enquiry(request):
    return render(request, 'enquiry.html')

def prayers(request):
    return render(request, 'prayer-request.html')