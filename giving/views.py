from django.shortcuts import render

# Create your views here.
def giving(request):
    return render(request, 'give.html')