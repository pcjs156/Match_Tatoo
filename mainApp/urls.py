from django.urls import path

from django.urls import path, include
from . import views
from accountApp import urls


urlpatterns = [
    path('', views.intro_view, name="intro"),
    path('main/', views.main_view, name="main"),
    path('accounts/', include('allauth.urls')),
]