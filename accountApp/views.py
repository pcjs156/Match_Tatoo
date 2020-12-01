import requests
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from match_tattoo.settings import DEBUG

from accountApp.forms import UserLoginForm, CustomerSignUpForm
from accountApp.tools import UserSignupChecker, TattooistSignUpForm

from tools import json_to_dict


# 로그인이 이미 되어 있는데 로그인을 시도하는 경우 이동되는 페이지
# 이미 로그인 되어 있는지 확인해야 함
# account/already_logged_in
def already_logged_in_view(request):
    if request.user.is_authenticated:
        return render(request, "already_logged_in.html")
    else:
        return redirect("main")


# 카카오 로그인 인증 class view
# DEBUG 모드일 때와 아닐 때의 도메인이 다르므로 참고할 것
class KakaoAuthView(View):
    def get(self, request):
        api_info = json_to_dict("kakao_rest_api_datas.json", "rest_api_key", "redirect_uri_debug", "redirect_uri")
        client_id = api_info["rest_api_key"]

        if DEBUG:
            redirect_uri = api_info["redirect_uri_debug"]
        else:
            redirect_uri = api_info["redirect_uri"]

        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code",
        )


class KakaoCallBackView(View):
    def get(self, request):
        try:
            code = request.GET.get("code")

            api_info = json_to_dict("kakao_rest_api_datas.json", "rest_api_key", "redirect_uri_debug", "redirect_uri")
            client_id = api_info["rest_api_key"]

            if DEBUG:
                redirect_uri = api_info["redirect_uri_debug"]
            else:
                redirect_uri = api_info["redirect_uri"]

            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )

            token_json = token_request.json()

            error = token_json.get("error", None)

            if error is not None:
                return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

            access_token = token_json.get("access_token")

            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers = {"Authorization": f"Bearer {access_token}"}
            )

            profile_json = profile_request.json()
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email", None)
            kakao_id = profile_json.get("id")

            print(profile_json, kakao_account, email, kakao_id)

            return JsonResponse(
                {"profile_json":profile_json,
                "kakao_account": kakao_account,
                "email": email,
                "kakao_id": kakao_id},
                status=200
            )

        except KeyError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
        except access_token.DoesNotExist:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)


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
            user = authenticate(request=request, username=username, password=password)

            # 존재하는 유저인 경우
            if user is not None:
                # 인증되지 않은 유저인 경우
                if not user.authenticated:
                    return redirect("kakao_auth", user.username)

                # 인증된 유저인 경우
                else:
                    login(request, user)
                    return redirect("main")
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form, 'login_failed':True})

    else:
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form, 'login_failed':False})


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


# 피시술자(customer) 회원가입 페이지
# 이미 로그인한 상태인지 확인해야 함 (else : already_logged_in_view)
# account/signup_customer
def signup_customer_view(request):
    # 로그인한 사용자를 차단
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
            login(request, user)
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
            login(request, user)
            return redirect("main")

    else:
        form = TattooistSignUpForm()
        content["form"] = form
        content["validity_check"] = UserSignupChecker(form, default=True)
        return render(request, 'signup_tattooist.html', content)