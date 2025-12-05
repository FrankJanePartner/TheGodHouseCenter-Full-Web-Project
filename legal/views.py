from django.shortcuts import render

# Create your views here.

def privacy(request):
    return render(request, 'legal/privacy-details.html')
    
def terms(request):
    return render(request, 'legal/terms-details.html')
        