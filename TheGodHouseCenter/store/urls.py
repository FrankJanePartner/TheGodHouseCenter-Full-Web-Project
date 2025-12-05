from django.urls import path

from .views import product_all, cart, checkout, success, delete_cart_item  # Ensure you have the correct view function

app_name = 'store'

urlpatterns = [
    path('', product_all, name='product_all'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('success/', success, name='success'),
    path('delete/<int:product_id>/', delete_cart_item, name='delete_cart_item'),  # Correct URL pattern
]
