from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # default django user model
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
