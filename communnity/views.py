from django.shortcuts import render

# Create your views here.
def churches(request):
    return render(request, 'men.html')

def units(request):
    return render(request, 'units.html')