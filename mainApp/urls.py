from django.urls import path

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.intro_view, name="intro"),
    path('main/', views.main_view, name="main"),
    path('search_result/', views.search_result_view, name="search_result"),
    path('accounts/', include('allauth.urls')),
    path('tattooist/', include('tattooistApp.urls')),
]