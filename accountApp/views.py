from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accountApp.forms import UserLoginForm, CustomerSignUpForm
from accountApp.tools import UserSignupChecker, TattooistSignUpForm
from allauth.socialaccount.views import SignupView

# 로그인이 이미 되어 있는데 로그인을 시도하는 경우 이동되는 페이지
# 이미 로그인 되어 있는지 확인해야 함
# account/already_logged_in
def already_logged_in_view(request):
    if request.user.is_authenticated:
        return render(request, "already_logged_in.html")
    else:
        return redirect("main")


# 로그인 페이지
# 이미 로그인한 상태인지 확인해야 함 (else : already_logged_in_view)
# account/login
def login_view(request):
    # 로그인한 사용자를 차단
    if request.user.is_authenticated:
        return redirect("already_logged_in")

    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = form.save()
            login(request,user,
                backend='allauth.account.auth_backends.AuthenticationBackend')
            if user is not None:
                login(request, user,
                backend='allauth.account.auth_backends.AuthenticationBackend')
                return redirect("main")

    else:
        form = UserLoginForm()
        backend='allauth.account.auth_backends.AuthenticationBackend'
        return render(request, 'login.html', {'form': form})


def __logout(request):
    logout(request)
    return redirect("main")


# 마이페이지
# account/mypage
@login_required(login_url="/account/login")
def mypage_view(request):
    return render(request, "mypage.html")


# 회원가입 전 유저 유형을 선택하는 페이지(시술자: tattooist / 피시술자: customer)
# 이미 로그인한 상태인지 확인해야 함 (else : already_logged_in_view)
# account/select_user_type
def select_user_type_view(request):
    # 로그인한 사용자를 차단
    if request.user.is_authenticated:
        return redirect("already_logged_in")

    return render(request, "select_user_type.html")

def social_signup_view(request):
    # 로그인한 사용자를 차단
    if request.user.is_authenticated:
        return redirect("already_logged_in")

    return render(request, "accounts/social/signup.html")


# 피시술자(customer) 회원가입 페이지
# 이미 로그인한 상태인지 확인해야 함 (else : already_logged_in_view)
# account/signup_customer
def signup_customer_view(request):
    # 로그인한 사용자를 차단
                    
    backend='allauth.account.auth_backends.AuthenticationBackend'

    if request.user.is_authenticated:
        return redirect("already_logged_in")

    content = dict()

    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST, request.FILES)
        validity_checker = UserSignupChecker(form)
        content["validity_check"] = validity_checker

        # 만약 False가 validity_check_dict.values에 있다면
        # 뭔가 문제가 생긴 것임으로 다시 입력해야 함
        if not validity_checker.is_valid():
            # 입력한 정보가 담겨 있는 form으로 갱신
            content["form"] = CustomerSignUpForm(request.POST, request.FILES)
            return render(request, 'signup_customer.html', content)

        else:
            user = form.save()
            user.save()
            login(request, user,
    backend='allauth.account.auth_backends.AuthenticationBackend')
            return redirect("main")

    else:
        form = CustomerSignUpForm()
        content["form"] = form
        content["validity_check"] = UserSignupChecker(form, default=True)
        return render(request, 'signup_customer.html', content)


# 시술자(tattooist) 회원가입 페이지
# 이미 로그인한 상태인지 확인해야 함 (else : already_logged_in_view)
# account/signup_tattooist
def signup_tattooist_view(request):
    # 로그인한 사용자를 차단
    if request.user.is_authenticated:
        return redirect("already_logged_in")

    content = dict()

    if request.method == 'POST':
        form = TattooistSignUpForm(request.POST, request.FILES)
        validity_checker = UserSignupChecker(form)
        content["validity_check"] = validity_checker

        # 만약 False가 validity_check_dict.values에 있다면
        # 뭔가 문제가 생긴 것임으로 다시 입력해야 함
        if not validity_checker.is_valid():
            # 입력한 정보가 담겨 있는 form으로 갱신
            content["form"] = TattooistSignUpForm(request.POST, request.FILES)
            return render(request, 'signup_tattooist.html', content)

        else:
            user = form.save()
            user.save()
            login(request, user,
            backend='allauth.account.auth_backends.AuthenticationBackend')
            return redirect("main")

    else:
        form = TattooistSignUpForm()
        content["form"] = form
        content["validity_check"] = UserSignupChecker(form, default=True)
        return render(request, 'signup_tattooist.html', content)




class AccountSignupView(SignupView):
    # Signup View extended

    # change template's name and path
    template_name = "templates/socialaccount/signup.html"
    
    def social_signup_view(request):
        # 로그인한 사용자를 차단
        if request.user.is_authenticated:
            return redirect("already_logged_in")

        return render(request, "socialaccount/signup.html")



account_signup_view = AccountSignupView.as_view()