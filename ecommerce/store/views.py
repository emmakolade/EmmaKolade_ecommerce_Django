from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib.auth.forms import UserCreationForm
from .form import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def home(request):

	context = {}
	return render(request, 'store/index.html', context)

def signUpPage(request):
	form = SignUpForm()

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid(): #validates the form
			user = form.save()

			username = form.cleaned_data.get('username')
			Customer.objects.create(
				user=user,
				) #creates a customer profile whenever they sign up.

			messages.success(request, 'Account Created Successfully for ' + username )
			return redirect('loginPage')
	context = {'form': form}
	return render(request, 'store/register.html', context)

def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'username or password is not correct')
			# return render(request, 'store/login.html', context)


	context = {}
	return render(request, 'store/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def collections(request):

	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	context = {'products':products, 'cartItems': cartItems}
	return render(request, 'store/collections.html', context)

def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		'items': items,
		'order': order,
		'cartItems': cartItems,
	}
	return render(request, 'store/cart.html', context)

def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	context = {
		'items': items,
		'order': order,
		'cartItems': cartItems,
	}
	return render(request, 'store/checkout.html', context)

def addedItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False) #to either create and order or get the customer order if it exist.
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()


	return JsonResponse('Item was added', safe=False)

# to process order and set the value to complete
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False) #to either create and order or get the customer order if it exist.

	else:
		customer, order = guestOrder(request, data)


	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	#check if the total from the frontend is the same with backend
	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	#value of the shipping
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			# city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment Complete', safe=False)


def menPage(request):
	context = {}
	return render(request, 'store/men.html', context)

def womenPage(request):
	context = {}
	return render(request, 'store/women.html', context)

