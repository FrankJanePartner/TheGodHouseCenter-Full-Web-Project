from .models import Legal

# Register your models here.
def legal(request):
    legal =  Legal.objects.all()
    context = {
        'legal':legal
    }
    return context
