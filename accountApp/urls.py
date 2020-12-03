from django.urls import path

from . import views

urlpatterns = [
    path("already_logged_in", views.already_logged_in_view, name="already_logged_in"),
    path("auth_complete", views.auth_complete_view, name="auth_complete"),
    path("kakao_auth/<str:username>", views.kakao_auth_view, name="kakao_auth"),
    path("kakao_callback", views.kakao_callback_view, name="kakao_callback"),
    path("login", views.login_view, name="login"),
    path("login_for_kakao_auth/<str:kakao_id>", views.login_for_kakao_auth_view, name="login_for_kakao_auth"),
    path("logout", views.__logout, name="logout"),
    path("mypage", views.mypage_view, name="mypage"),
    path("select_user_type", views.select_user_type_view, name="select_user_type"),
    path("signup_customer", views.signup_customer_view, name="signup_customer"),
    path("signup_tattooist", views.signup_tattooist_view, name="signup_tattooist"),
]
