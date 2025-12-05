from django.shortcuts import get_object_or_404, render
from core.models import Location
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder, delete
import os  # Importing the os module for interacting with the operating system
import logging  # Importing the logging module to log information and errors
import requests  # Importing the requests module to make HTTP requests
import phonenumbers  # Importing phonenumbers for handling phone number formatting
from django_countries import countries  # Importing countries to get country data
from django.views.decorators.csrf import csrf_exempt  # Importing CSRF exemption decorator

def product_all(request):
    # Retrieve cart data for the current user or guest
    data = cartData(request)
    
    # Extract cart items, order details, and items from the cart data
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Get all products from the database
    products = Product.objects.all()
    # Prepare context data to be passed to the template
    context = {'products': products, 'cartItems': cartItems}
    
    # Corrected indentation of return statement
    return render(request, 'store/books-merchants.html', context)


def cart(request):
    # Retrieve cart data for the current user or guest
    data = cartData(request)
    
    # Extract cart items, order details, and items from the cart data
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
	
    # print("Items in Cart:", items)

    # Prepare context data to be passed to the cart template
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    # Render the cart template with the context data
    return render(request, 'store/cart.html', context)


def checkout(request):
    """
    Handles the checkout process.
    :param request: HttpRequest object.
    :return: Rendered checkout page or JSON response with rates.
    """
    # basket = Basket(request)  # Create a basket instance for the current session
    
    # Retrieve cart data for the current user or guest
    data = cartData(request)

    # Extract cart items, order details, and items from the cart data
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    location = Location.objects.all()  # Retrieve all locations from the Location model
    countries_list = list(countries)  # Get the list of countries
    supported_countries = phonenumbers.SUPPORTED_REGIONS  # Get the supported phone number regions
    country_codes = []  # Initialize a list for country codes

    # Get country codes and country names
    for country in supported_countries:  # Loop through supported countries
        country_code = phonenumbers.country_code_for_region(country)  # Get country code for the region
        if country_code:  # If a country code is found
            country_codes.append((f"+{country_code}", country))  # Append in format (+Code, Country Name)
    
    # Sort the country codes numerically by removing the '+' sign for comparison
    sorted_country_codes = sorted(country_codes, key=lambda x: int(x[0].replace("+", "")))

    # List of Nigerian states and their abbreviations
    NG_STATES = [
        ('AB', 'Abia'),
        ('AD', 'Adamawa'),
        ('AK', 'Akwa Ibom'),
        ('AN', 'Anambra'),
        ('BA', 'Bauchi'),
        ('BE', 'Benue'),
        ('BO', 'Borno'),
        ('CO', 'Cross River'),
        ('DE', 'Delta'),
        ('EB', 'Ebonyi'),
        ('ED', 'Edo'),
        ('EK', 'Ekiti'),
        ('EN', 'Enugu'),
        ('GO', 'Gombe'),
        ('IM', 'Imo'),
        ('JO', 'Jigawa'),
        ('KE', 'Kano'),
        ('KD', 'Kaduna'),
        ('KO', 'Kogi'),
        ('KW', 'Kwara'),
        ('LA', 'Lagos'),
        ('NAS', 'Nasarawa'),
        ('NI', 'Niger'),
        ('OG', 'Ogun'),
        ('ON', 'Ondo'),
        ('OS', 'Osun'),
        ('OY', 'Oyo'),
        ('PL', 'Plateau'),
        ('RI', 'Rivers'),
        ('SO', 'Sokoto'),
        ('TAR', 'Taraba'),
        ('YOB', 'Yobe'),
        ('ZA', 'Zamfara'),
    ]

    # Render the checkout page with necessary data for the frontend
    context = {
        'countries': countries_list,
        'country_codes': sorted_country_codes,
        'ng_states': NG_STATES,
        'location': location,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'store/store-checkout.html', context)


def updateItem(request):
	# Load the JSON data from the request body
	data = json.loads(request.body)
	# Extract product ID and action (add/remove) from the data
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	# Get the customer associated with the logged-in user
	customer = request.user.customer
	# Retrieve the product based on the provided product ID
	product = Product.objects.get(id=productId)
	# Get or create an order for the customer that is not complete
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	# Get or create an order item for the specified product in the order
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	# Update the quantity of the order item based on the action
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	# Save the updated order item
	orderItem.save()

	# If the quantity is less than or equal to zero, delete the order item
	if orderItem.quantity <= 0:
		orderItem.delete()

	# Return a JSON response indicating the item was added
	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	# Generate a unique transaction ID based on the current timestamp
	transaction_id = datetime.datetime.now().timestamp()
	# Load the JSON data from the request body
	data = json.loads(request.body)

	# Check if the user is authenticated
	if request.user.is_authenticated:
		# Get the customer associated with the logged-in user
		customer = request.user.customer
		# Get or create an order for the customer that is not complete
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		# If the user is not authenticated, create a guest order
		customer, order = guestOrder(request, data)

	# Extract the total amount from the form data
	total = float(data['form']['total'])
	# Set the transaction ID for the order
	order.transaction_id = transaction_id

	# Check if the total matches the order's cart total
	if total == order.get_cart_total:
		# If they match, mark the order as complete
		order.complete = True
	# Save the order with the updated information
	order.save()

	# If the order requires shipping, create a shipping address
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)

	# Return a JSON response indicating the payment was submitted
	return JsonResponse('Payment submitted..', safe=False)


def delete_cart_item(request, product_id):
    if request.method == 'DELETE':
        product = Product.objects.get(id=product_id)  # Get the product instance
        message = product.delete_product()  # Call the delete method
        return JsonResponse({'message': message}, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)  # Handle other methods


def success(request):
    """
    Renders the success page after a successful transaction.
    :param request: HttpRequest object.
    :return: Rendered success page.
    """
    return render(request, 'store/store-success.html')  # Render the success page template


