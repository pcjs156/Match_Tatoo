from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction
from .models import Customer
from allauth.socialaccount.forms import SignupForm
from allauth.account.forms import SignupForm
from allauth.account.forms import BaseSignupForm
class MyCustomSignupForm(SignupForm):

    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'email',
                  'nickname', 'introduce', 'user_image']
                  
    @transaction.atomic
    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super().save()
        # Add your own processing here.
        # You must return the original result.
        return user
class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'email',
                  'nickname', 'introduce', 'user_image']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_customer = True
        user.save()
        return user


class TattooistSignUpForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'email',
                  'nickname', 'introduce', 'user_image', 'contact', 'location']

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_tattooist = True
        user.save()
        return user
