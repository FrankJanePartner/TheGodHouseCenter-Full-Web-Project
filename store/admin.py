from django.contrib import admin
from .models import Product, ProductDimension, ProductDimensionValue, Customer, Order, OrderItem


class ProductDimensionValueInline(admin.TabularInline):
    model = ProductDimensionValue


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'in_stock']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [
        ProductDimensionValueInline,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDimension)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
