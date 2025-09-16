from .models import Church, Unit

# Create your views here.
def churches(request):
    return {
        'churches': Church.objects.all(),
        "units" : Unit.objects.all()
    }