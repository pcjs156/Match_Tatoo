from django.shortcuts import render

# 인트로 페이지
# /
def intro_view(request):
    return render(request, "intro.html")

# 메인 페이지
# /main
def main_view(request):
    return render(request, "main.html")
