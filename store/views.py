from django.shortcuts import get_object_or_404, render, redirect
from core.models import Location
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
import json
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder, delete
import os  # Importing the os module for interacting with the operating system
import logging  # Importing the logging module to log information and errors
import requests  # Importing the requests module to make HTTP requests
import phonenumbers  # Importing phonenumbers for handling phone number formatting
from django_countries import countries  # Importing countries to get country data
from django.views.decorators.csrf import csrf_exempt  # Importing CSRF exemption decorator
from .shipbubble import ShipBubble, API_KEY


SBAPI = ShipBubble(API_KEY)

def edit_phone_number(phone_number):
    # Check if the phone number is a string and has 11 digits
    if isinstance(phone_number, str) and len(phone_number) == 11:
        # Remove the first digit
        return phone_number[1:]
    else:
        return phone_number  # Return the original number if it doesn't meet the criteria


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
    return render(request, 'books-merchants.html', context)


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
    return render(request, 'cart.html', context)


def checkout(request):
    """
    Handles the checkout process.
    :param request: HttpRequest object.
    :return: Rendered checkout page or JSON response with rates.
    """
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

    sender_address = "2 Indian Street Beside Mansal Hotel by Regal Clinic Off Jakpa Road, Effurun-Warri, Delta, Nigeria"
    sender_phone_number = "+2348050269090"
    sender_email = "info@godhouse.com"
    sender_name = "Godhouse missions"

    now = timezone.now()
    pickup_date = (now + timedelta(days=6)).date().strftime('%Y-%m-%d')

    if request.method == "POST":
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone_country_code = request.POST.get('phone_country_code')
        phone_number = request.POST.get('phone_number')
        delivery_type = request.POST.get('delivery_type')
        plocation = request.POST.get('pickup_location')
        country = request.POST.get('country')
        state = request.POST.get('state')
        other_state = request.POST.get('other_state')
        city = request.POST.get('lga-input')
        address = request.POST.get('delivery_address')
        proofOfPayment = request.FILES.get('image')
        totalCost = order['get_cart_total']

        if country == "Nigeria":
            receiverAddress = f"{address}, {city}, {state}, {country}"
        else:
            receiverAddress = f"{address}, {city}, {other_state}, {country}"

        edited_phonenumber = edit_phone_number(phone_number)
        phone = f"{phone_country_code} {edited_phonenumber}"

        totalCost = order['get_cart_total']

        # Validate sender's address
        validate_sender_address = SBAPI.validateAddress(sender_name, sender_email, sender_phone_number, sender_address)
        if validate_sender_address["status"] == "success":
            sender_address_code = validate_sender_address["data"].get('address_code')
        else:
            print("Sender Address Validation Failed:", validate_sender_address["message"])
            sender_address_code = None  # Set to None or handle accordingly

        # Validate receiver's address
        validate_receiver_address = SBAPI.validateAddress(full_name, email, phone, receiverAddress)
        if validate_receiver_address["status"] == "success":
            receiver_address_code = validate_receiver_address["data"].get('address_code')
        else:
            print("Receiver Address Validation Failed:", validate_receiver_address["message"])
            receiver_address_code = None  # Set to None or handle accordingly


        category_id = SBAPI.getCategories()
        category_ids = [item['category_id'] for item in category_id['data'] if item['category'] == 'Fashion wears']


        package_items = []  # Initialize an empty list to store package_item
        package_dimensions = {
            'length': 0,
            'width': 0,
            'height': 0,
        }

        for item in items:
            product = Product.objects.get(id=item['id'])  # Ensure product is fetched here
            package_dimension = ProductDimensionValue.objects.filter(product=product)

            # Initialize variables to store dimensions
            total_length = 0
            total_width = 0
            total_height = 0
            itemWeight = 0

            for dimension in package_dimension:
                if dimension.Dimension.name == 'weight':
                    itemWeight = dimension.value
                elif dimension.Dimension.name == 'length':
                    total_length += float(dimension.value)
                elif dimension.Dimension.name == 'width':
                    total_width += float(dimension.value)
                elif dimension.Dimension.name == 'height':
                    total_height += float(dimension.value)

            description = product.description[:10]  # Get a short description
            amount = product.price
            quantity = item['quantity']

            package_items.append({
                'name': full_name,
                'description': description,
                'unit_weight': itemWeight,
                'unit_amount': amount,
                'quantity': quantity,
            })

            # Accumulate total dimensions
            package_dimensions['length'] += total_length
            package_dimensions['width'] += total_width
            package_dimensions['height'] += total_height

        
        if 'get_rates' in request.POST:
            rates = getRates(request, sender_address_code, receiver_address_code, pickup_date, category_ids, package_items, package_dimensions)
            rates_response = getRates(request, sender_address_code, receiver_address_code, pickup_date, category_ids, package_items, package_dimensions)
    
            # Assuming getRates returns a dictionary
            if rates_response['status'] == 'success':
                ratesData = rates_response.get('data', {})
                print(ratesData)
                return JsonResponse({'status': 'success', 'rates': ratesData})
            else:
                print("Error: 'data' key not found in rates response:", rates_response.get('message', 'No message'))
                return JsonResponse({'status': 'error', 'message': rates_response.get('message', 'Failed to get rates')})

        
        elif 'place_order' in request.POST:
            if  delivery_type == "Personal Pickup":
                customer = Customer.objects.create(
                    name=full_name,
                    email=email,
                    phone_number_code=phone_country_code,
                    phone_number=phone_number
                    )
                if proofOfPayment is not None:
                    order = Order.objects.create(
                        customer=customer,
                        delivery_type='Personal Pickup',
                        pickup_location=plocation,
                        total_cost=totalCost,
                        payment_proof=proofOfPayment,
                        )
                for item in items:
                    product = Product.objects.get(id=item['id'])
                    orderItem = OrderItem.objects.create(
                        order=order, 
                        product=product, 
                        quantity=item['quantity']
                        ) # Access the quantity for each item in the list
                    
                
                
                return redirect('store:success')
            
            else:
                
                couriers = rates['data']["couriers"]
                token = rates['data']['request_token']
                for index, courier in enumerate(couriers):
                    if courier['courier_name'] == "Millie Express":
                        one = index

                service_code = couriers[one]["service_code"]
                insurance = couriers[one]["insurance"]["code"]
                courier_id = couriers[one]["courier_id"]
                
                r12 = SBAPI.createShipment(token, service_code, courier_id, insurance)

                return redirect('store:success')

        
        # if 'get_rates' in request.POST:
        #     return get_shipping_rates(request, full_name, address, city, country, order['get_cart_total'])

        # if 'submit_order' in request.POST:
        #     return submit_order(request, full_name, email, phone_number, country_code, country, state, city, address)
    return render(request, 'store-checkout.html', context)


def success(request):
    """
    Renders the success page after a successful transaction.
    :param request: HttpRequest object.
    :return: Rendered success page.
    """
    return render(request, 'store-success.html')  # Render the success page template



def getRates(request, sender_address_code, receiver_address_code, pickup_date, category_ids, package_items, package_dimensions):
    """
    Handles the get rate API request.
    :param request: HttpRequest object.
    :return: Rendered JSON response with rates or rendered template.
    """
    # Convert Decimal values to float in package_items and package_dimensions
    for item in package_items:
        item['unit_amount'] = float(item['unit_amount'])  # Assuming this is a Decimal
        item['unit_weight'] = float(item['unit_weight'])  # Assuming this is a Decimal

    # Convert package dimensions
    package_dimensions['length'] = float(package_dimensions['length'])
    package_dimensions['width'] = float(package_dimensions['width'])
    package_dimensions['height'] = float(package_dimensions['height'])

    rates = SBAPI.getShippingRate(sender_address_code, receiver_address_code, pickup_date, category_ids, package_items, "Handle with care!", package_dimensions, "dropoff")

    
    return JsonResponse({'status': 'success', 'pickup_date': str(pickup_date)})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)


