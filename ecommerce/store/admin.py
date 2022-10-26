from django.contrib import admin
from .models import *

class SubscribedUsersAdmin(admin.ModelAdmin):
	list_display = ('email', 'name', 'created_date')


# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(SubscribedUsers, SubscribedUsersAdmin)


