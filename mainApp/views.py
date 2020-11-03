from django.shortcuts import render

def intro_view(request):
    return render(request, "intro.html")

def main_view(request):
    return render(request, "main.html")