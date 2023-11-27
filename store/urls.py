from django.urls import path

from .views import product_all, product_detail

app_name = 'store'

urlpatterns = [
    path('', product_all, name='product_all'),
    path('item/<slug:slug>', product_detail, name='product_detail'),
]
 