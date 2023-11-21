from django.shortcuts import render
from .models import Church, Unit

# Create your views here.
def churches(request):
    churches = Church.objects.all()
    return render(request, 'men.html', {'churches':churches})

def units(request):
    units = Unit.objects.all()
    return render(request, 'units.html', {"units":units})