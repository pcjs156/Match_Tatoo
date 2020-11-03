from django.urls import path

from . import views

urlpatterns = [
    path('', views.intro_view, name="intro"),
    path('main/', views.main_view, name="main"),
]