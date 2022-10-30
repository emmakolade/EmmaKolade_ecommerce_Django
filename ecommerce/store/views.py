from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib.auth.forms import UserCreationForm
from .form import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib.auth.decorators import login_required

from .models import *
from .utils import cookieCart, cartData, guestOrder

from django.views import View

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
def home(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
			'items': items,
			'order': order,
			'cartItems': cartItems,
		}
	return render(request, 'store/index.html', context)

# @login_required(login_url= 'home')
def loginRegister(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = SignUpForm()

		if request.method == 'POST':
			# register/signup
			form = SignUpForm(request.POST)
			if form.is_valid(): # validates the form
				user = form.save()

				username = form.cleaned_data.get('username')
				Customer.objects.create(
					user=user,
					name=user.username
					) # creates a customer profile whenever they sign up.

				messages.success(request, 'Account Created Successfully for ' + username )
			# login
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'credentials invalid')

		context = {'form': form}
		return render(request, 'store/loginSignup.html', context)


def logoutUser(request):
	logout(request)
	return redirect('home')

class collections(View):
	def get(self, request):
		data = cartData(request)
		cartItems = data['cartItems']
		products = Product.objects.all()
		context = {'products':products, 'cartItems': cartItems}
		return render(request, 'store/collections.html', context)

# def collections(request):

# 	data = cartData(request)
# 	cartItems = data['cartItems']

# 	products = Product.objects.all()
# 	context = {'products':products, 'cartItems': cartItems}
# 	return render(request, 'store/collections.html', context)

class cart(View):
	def get(self, request):
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

class checkout(View):
	def get(self, request):

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


def subscribe(request):
	if request.method == 'POST':
		name = request.POST.get('name', None)
		email = request.POST.get('email', None)

		if not name or not email:
			messages.error(request, "enter an appropraite email to subscribe")
			return redirect('home')

		if get_user_model().objects.filter(email=email).first():
			messages.error(request, f"your email {email} has been used.")
			return redirect(request.META.get("HTTP_REFERER", "home"))

		# checks if the email is not in the subscribed list
		subscribe_user = SubscribedUsers.objects.filter(email=email).first()
		if subscribe_user:
			messages.error(request, f"{email} email address is already subscriber.")
			return redirect(request.META.get("HTTP_REFERER", "home"))
		try:
			validate_email(email)
		except ValidationError as e:
			messages.error(request, e.messages[0])
			return redirect("home")

		subscribe_model_instance = SubscribedUsers()
		subscribe_model_instance.name = name
		subscribe_model_instance.email = email
		subscribe_model_instance.save()
		messages.success(request, f' your email {email} was successfully subscribed to our newsletter!')
		return redirect(request.META.get("HTTP_REFERER", "home"))


def menPage(request):
	context = {}
	return render(request, 'store/men.html', context)

def womenPage(request):
	context = {}
	return render(request, 'store/women.html', context)

# all auth
def siginRedirect(request):
	messages.error(request, "something went wrong, it may be that you already have an account")
	return redirect("home")



def productDetails(request):
	details = ProductDetail.objects.all()
	context = {}
	return render(request, 'store/productdetail.html', context)


# class collections(View):
# 	def get(self, request):
# 		data = cartData(request)
# 		cartItems = data['cartItems']
# 		products = Product.objects.all()
# 		context = {'products':products, 'cartItems': cartItems}
# 		return render(request, 'store/collections.html', context)

# def collections(request):

# 	data = cartData(request)
# 	cartItems = data['cartItems']

# 	products = Product.objects.all()
# 	context = {'products':products, 'cartItems': cartItems}
# 	return render(request, 'store/collections.html', context)

