from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('collections/', views.collections.as_view(), name="collections"),
    path('cart/', views.cart.as_view(), name="cart"),
    # path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logoutUser, name="logout"),
    # path('register/', views.signUpPage, name="signUpPage"),
    path('login/', views.loginRegister, name="login"),
    path('checkout/', views.checkout.as_view(), name="checkout"),
    path('added_item/', views.addedItem, name="added_item"),
    path('process_order/', views.processOrder, name="added_item"),
    path('men/', views.menPage, name="men"),
    path('women/', views.womenPage, name="women"),

    path('details/', views.productDetails, name="details"),

    path('subcribe/', views.subscribe, name="subscribe"),
    path('social/signup/', views.siginRedirect, name="siginRedirect"),



    # reset password
    path('reset_password', auth_views.PasswordResetView.as_view(
        template_name="store/resetPassword.html"), name="reset_password"),

    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(
        template_name="store/resetPasswordSent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="store/resetPasswordForm.html"), name="password_reset_confirm"),

    path('reset_password', auth_views.PasswordResetCompleteView.as_view(
        template_name="store/resetPasswordDone.html"), name="password_reset_complete"),
]
