from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# 로그인이 이미 되어 있는데 로그인을 시도하는 경우 이동되는 페이지
# 이미 로그인 되어 있는지 확인해야 함
# account/already_logged_in
def already_logged_in_view(requst):
    return render(requst, "already_logeed_in.html")


# 로그인 페이지
# 이미 로그인한 상태인지 확인해야 함 (else : already_logged_in_view)
# account/login
def login_view(request):
    return render(request, "login.html")


# 마이페이지
# account/mypage
@login_required(login_url="/account/login")
def mypage_view(request):
    return render(request, "mypage.html")


# 회원가입 전 유저 유형을 선택하는 페이지(시술자: tattooist / 피시술자: customer)
# 이미 로그인한 상태인지 확인해야 함 (else : login)
# account/select_user_type
def select_user_type_view(request):
    return render(request, "select_user_type.html")


# 피시술자(customer) 회원가입 페이지
# 이미 로그인한 상태인지 확인해야 함 (else : login)
# account/signup_customer
def signup_customer_view(request):
    return render(request, "signup_customer.html")


# 시술자(tattooist) 회원가입 페이지
# 이미 로그인한 상태인지 확인해야 함 (else : login)
# account/signup_tattooist
def signup_tattooist_view(request):
    return render(request, "signup_tattooist.html")