from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("mypage", views.mypage_view, name="mypage"),
    path("select_user_type", views.select_user_type_view, name="select_user_type"),
    path("signup_customer", views.signup_customer_view, name="signup_customer"),
    path("signup_tattooist", views.signup_tattooist_view, name="signup_tattooist"),
]
