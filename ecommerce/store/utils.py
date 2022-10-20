import json
from .models import *

from django.core.exceptions import ObjectDoesNotExist


def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart']) #get the cookie value
	except:
		cart = {}

	items = []
	order = {
		'get_cart_total' : 0,
		'get_cart_items': 0,
		'shipping': False,

	}
	cartItems = order['get_cart_items']

	for i in cart:
		# to ensure that nothing goes wrong with the code below i will usee the try/except
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'product':{
					'id': product.id,
					'name': product.name,
					'price': product.price,
					'CollectionsURL': product.CollectionsURL,
				},
				'quantity': cart[i]['quantity'],
				'get_total': total,
			}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
	return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
	if request.user.is_authenticated:
		# if hasattr(request.user, 'customer'):
		# customer = User.objects.get(pk=request.user.id).customer
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False) #to either create and order or get the customer order if it exist.
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	# else:
	# 	items = []
	return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
	print('user is not logged in')


	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
		email=email,
		) #if user doesnt want to create an account
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)
	# loop through items, add items to the database and create them and attach to order
	for item in items:
		product = Product.objects.get(id=item['product']['id'])

		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity']
			)
	return customer, order
