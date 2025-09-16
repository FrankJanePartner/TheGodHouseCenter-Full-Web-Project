from .models import HeaderInfo
from communnity.models import Church

def globalContext(request):
    churches = Church.objects.all()
    header = HeaderInfo.objects.all()
    context = {
        'churches':churches,
        'header':header
    }
    return context
