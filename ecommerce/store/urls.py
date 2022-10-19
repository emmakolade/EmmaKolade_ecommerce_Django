from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('collections/', views.collections, name="collections"),
	path('cart/', views.cart, name="cart"),
	path('login/', views.loginPage, name="loginPage"),
	path('logout/', views.logoutUser, name="logout"),
	path('register/', views.signUpPage, name="signUpPage"),
	path('checkout/', views.checkout, name="checkout"),
	path('added_item/', views.addedItem, name="added_item"),
	path('process_order/', views.processOrder, name="added_item"),
]