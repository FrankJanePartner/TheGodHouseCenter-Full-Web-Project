from django.shortcuts import render, get_object_or_404
from .models import Church, Unit

# Create your views here.
def churches(request, slug):
    church = get_object_or_404(Church, slug=slug)
    context = {
        'church': church,
    }
    return render(request, 'community/men.html', context)
    
def units(request):
    unit = Unit.objects.all()
    return render(request, 'community/units.html', {"unit":unit})