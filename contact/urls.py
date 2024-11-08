from django.urls import path
from .views import contact, enquiry, prayers, testimony

app_name = 'contact'
urlpatterns = [
    path('', contact, name='contact'),
    path('enquiry/', enquiry, name='enquiry'),
    path('prayers/', prayers, name='prayers'),
    path('share-your-testimony/', testimony, name='testimony')
]
