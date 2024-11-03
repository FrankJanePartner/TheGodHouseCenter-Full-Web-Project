from django.shortcuts import render, get_object_or_404
from .models import Church, Unit

# Create your views here.
def churches(request, slug):
    churches = get_object_or_404(Church, slug=slug)
    context = {
        'churches': churches,
    }
    
    return render(request, 'men.html', context)

def units(request):
    units = Unit.objects.all()
    return render(request, 'units.html', {"units":units})