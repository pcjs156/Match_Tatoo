from django.urls import path

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.intro_view, name="intro"),
    path('main/', views.main_view, name="main"),
    path('accounts/', include('allauth.urls')),
]