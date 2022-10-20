from django.db import models
from django.contrib.auth.models import User




# Create your models here.

# customer model
class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


# product model
class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	digital = models.BooleanField(default=False, null=True, blank=False) #if the item is digital it doesnt need to be shipped
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property # allows access to Product as an attribute rather than a method
	def CollectionsURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

# Order model
# this is basically the cart, every items added to the cart is stored in Order
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # customer can have multiple orders.
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)



	def __str__(self):
		return str(self.id)
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping


	# total value of the cart
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems]) #detect the amount of items in the cart
		return total

# OrderItem model (this are items within the cart)
# orderitem links btw the order and the product/item.
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	# the total value of the order item
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


# Shipping model
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=True)
	# city = models.CharField(max_length=200, null=True)
	state = models.CharField(max_length=200, null=True)
	zipcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

