from django.urls import path

from django.urls import path, include
from . import views
from accountApp import urls

from .views import account_signup_view
from . import views

urlpatterns = [
    path("already_logged_in", views.already_logged_in_view, name="already_logged_in"),
    path("login", views.login_view, name="login"),
    path("logout", views.__logout, name="logout"),
    path("mypage", views.mypage_view, name="mypage"),
    path("select_user_type", views.select_user_type_view, name="select_user_type"),
    path("signup_customer", views.signup_customer_view, name="signup_customer"),
    path("signup_tattooist", views.signup_tattooist_view, name="signup_tattooist"),
    
     # override the SignupView of django-allauth
    path("accounts/social/signup", views.AccountSignupView , name = 'social_signup'),
]
