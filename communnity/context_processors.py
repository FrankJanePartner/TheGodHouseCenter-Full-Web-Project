from .models import Church

# Create your views here.
def churches(request):
    return {
        'churches': Church.objects.all()
    }