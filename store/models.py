from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Customer(models.Model):
    name = models.CharField(max_length=100)  # Full name from the form
    email = models.EmailField(blank=True)  # Email
    phone_number_code = models.CharField(max_length=5, blank=True)  # Phone number
    phone_number = models.CharField(max_length=15)  # Phone number

    def __str__(self):
        # String representation of the Customer object, returns the customer's name.
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='Apostle T. D. Philips')
    description = HTMLField()
    image = models.FileField(
        upload_to='images/',
        default='images/default.png'
    )
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
        
    @property
    def imageURL(self):
        # Property to get the URL of the product image.
        try:
            url = self.image.url
        except:
            # If the image does not exist, return an empty string.
            url = ''
            return url

    def __str__(self):
        return self.product_name



class ProductDimension(models.Model):
    """
    The Product Dimension Table contains product
    specifiction or features for the product types.
    """

    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Dimension")
        verbose_name_plural = _("Product Dimensions")

    def __str__(self):
        return self.name
    
class ProductDimensionValue(models.Model):
    """
    The Product Dimension Value table holds each of the
    products individual Dimension or bespoke features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Dimension = models.ForeignKey(ProductDimension, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product Dimension value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Dimension Value")
        verbose_name_plural = _("Product Dimension Values")

    def __str__(self):
        return self.value



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)  # Many-to-many relation with Product through OrderItem
    delivery_type = models.CharField(max_length=50, choices=[('Personal Pickup', 'Personal Pickup'), ('Express Delivery', 'Express Delivery')])  # Delivery type from form
    pickup_location = models.CharField(max_length=100, blank=True)  # Pickup location for personal pickup
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # Total cost (product + shipping)
    payment_proof = models.FileField(upload_to='payment_proofs/', blank=True, null=True)  # File upload for proof of payment
    created_at = models.DateTimeField(auto_now_add=True, blank=True)  # Timestamp for order creation

    def __str__(self):
        return f"Order from {self.customer.name}"

    @property
    def shipping(self):
        # Property to determine if the order requires shipping.
        shipping = False
        # Get all order items associated with this order.
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            # if i.order.delivery_type is 'Express Delivery' then shipping is true
            if i.order.delivery_type == 'Express Delivery':
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        # Property to calculate the total price of all items in the cart.
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        # Property to count the total number of items in the cart.
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Reference to the order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Reference to the product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the order

    @property
    def get_total(self):
        # Property to calculate the total price for this order item (price * quantity).
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    # A foreign key relationship to the Customer model, allowing each shipping address to be associated with a customer.
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    # A foreign key relationship to the Order model, allowing each shipping address to be associated with an order.
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    delivery_address = models.TextField(blank=True, null=True)  # Delivery address for express delivery
    lga = models.CharField(max_length=100, blank=True, null=True)  # Local Government Area (if provided)
    country = models.CharField(max_length=100, blank=True)  # Country field from the form
    state = models.CharField(max_length=100, blank=True, null=True)  # State for Nigeria or other states for other countries
    # The date and time when the shipping address was added, automatically set when created.
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the ShippingAddress object, returns the address.
        return self.delivery_address
