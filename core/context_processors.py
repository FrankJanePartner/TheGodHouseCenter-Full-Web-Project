from .models import Category

def categories(request):
    # Adjust your filtering logic based on an existing field (e.g., 'name')
    return {"categories": Category.objects.filter(name='name')}
