import json
from .models import *

def cookieCart(request):
	# Initialize an empty cart for non-logged-in users
	try:
		# Attempt to load the cart from cookies
		cart = json.loads(request.COOKIES['cart'])
	except:
		# If loading fails (e.g., no cart exists), create an empty cart
		cart = {}
		print('CART:', cart)

	# Initialize items list and order summary
	items = []
	order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
	cartItems = order['get_cart_items']

	# Iterate through each item in the cart
	for i in cart:
		# Use try block to handle potential errors (e.g., product not found)
		try:
			# Check if the item quantity is greater than zero
			if (cart[i]['quantity'] > 0):  # Items with negative quantity = freebies
				cartItems += cart[i]['quantity']  # Update total cart items

				# Retrieve the product from the database using its ID
				product = Product.objects.get(id=i)



				# Calculate the total price for this item
				total = (product.price * cart[i]['quantity'])

				# Update the order summary with totals
				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				# Create a dictionary for the item details
				item = {
					'id': product.id,
					'product': {
						'id': product.id,
						'name': product.product_name,
						'price': product.price,
						'imageURL': product.image.url,
						'description': product.description,
						'amount': product.price
					},
					'quantity': cart[i]['quantity'],
					'get_total': total,
				}
				# Add the item to the items list
				items.append(item)

				# Check if the product requires shipping
				# to find out if other shipping is required we need to check the order model and see if delivery_type == 'Express Delivery'
				order['shipping'] = product.order.shipping

		except:
			# If an error occurs (e.g., product not found), skip this item
			pass

	# Return the cart summary including items, total items, and order details
	return {'cartItems': cartItems, 'order': order, 'items': items}



def cartData(request):
	cookieData = cookieCart(request)
	cartItems = cookieData['cartItems']  # Get total items from cookie data
	order = cookieData['order']  # Get order details from cookie data
	items = cookieData['items']  # Get items from cookie data

	# Return the cart summary including items, total items, and order details
	return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
	# Extract name and email from the provided data
	name = data['form']['name']
	email = data['form']['email']

	# Get the cart data for the guest user
	cookieData = cookieCart(request)
	items = cookieData['items']  # Get items from the cart

	# Create a new customer entry or retrieve existing one based on email
	customer, created = Customer.objects.get_or_create(
		email=email,
	)
	customer.name = name  # Set the customer's name
	customer.save()  # Save the customer object

	# Create a new order for the customer
	order = Order.objects.create(
		customer=customer,
		complete=False,
	)

	# Iterate through each item in the cart to create order items
	for item in items:
		# Retrieve the product from the database using its ID
		product = Product.objects.get(id=item['id'])
		# Create an order item for each product in the order
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=(item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']),  # Handle negative quantity for freebies
		)
	# Return the customer and the created order
	return customer, order

def delete(request, product_id):
	"""
	Delete an item from the cart session data.
	"""
	# Attempt to load the cart from cookies
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	# Remove the product from the cart if it exists
	if product_id in cart:
		cart.pop(product_id, None)
		print(f'Product {product_id} removed from cart.')

	# Update the cookie with the new cart
	request.COOKIES['cart'] = json.dumps(cart)
	return cart  # Return the updated cart for further processing

def clear(self):
	"""
	Remove the basket from the session.
	"""
	self.session.pop('cart', None)
	self.save()