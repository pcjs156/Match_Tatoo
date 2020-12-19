from datetime import datetime

import requests
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

from accountApp.AccountErrorHandler import AlreadyAuthenticatedCustomer
from accountApp.models import Customer
from matchingApp.models import Matching
from tattooistApp.models import Review
from match_tattoo.settings import DEBUG

from accountApp.forms import UserLoginForm, CustomerSignUpForm
from accountApp.tools import UserSignupChecker, TattooistSignUpForm

from tools import json_to_dict
from .tools import kakao_encrypt, kakao_decrypt


# 로그인이 이미 되어 있는데 로그인을 시도하는 경우 이동되는 페이지
# 이미 로그인 되어 있는지 확인해야 함
# account/already_logged_in
def already_logged_in_view(request):
    if request.user.is_authenticated:
        return render(request, "already_logged_in.html")
    else:
        return redirect("main")

# 카카오 인증을 완료했을 때 이동하는 페이지
def auth_complete_view(request):
    return render(request, "auth_complete.html")

# 카카오 로그인 페이지로 이동시키는 뷰
# 단, 존재하지 않는 아이디이거나 이미 인증을 거친 경우 main페이지로 리다이렉트 시킴
# DEBUG 모드일 때와 아닐 때의 도메인이 다르므로 참고할 것
def kakao_auth_view(request, username: str):
    # 입력된 아이디를 가지고 있는 유저를 찾음
    try:
        user = Customer.objects.get(username=username)
        # 이미 인증을 거친 유저인 경우
        if user.authenticated:
            raise AlreadyAuthenticatedCustomer

    # 만약 해당 아이디를 가진 유저가 존재하지 않는 경우
    except Customer.DoesNotExist:
        print("Invalid access ocurred.")
        print("User does not exist.")
        print(f"username: {username}")
        print(f"datetime: {datetime.now()}")
        return redirect("main")
    # 이미 인증을 거친 유저인 경우
    except AlreadyAuthenticatedCustomer:
        print("Invalid access ocurred.")
        print("User has been authenticated.")
        print(f"username: {username}")
        print(f"datetime: {datetime.now()}")
        return redirect("main")

    # 위의 조건에 해당하지 않는 경우, 카카오 로그인 페이지로 이동시킴
    if request.method == "GET":
        api_info = json_to_dict("kakao_rest_api_datas.json", "rest_api_key", "redirect_uri_debug", "redirect_uri")
        client_id = api_info["rest_api_key"]

        if DEBUG:
            redirect_uri = api_info["redirect_uri_debug"]
        else:
            redirect_uri = api_info["redirect_uri"]

        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code",
        )


# kakao_auth로부터 인증 토큰을 받아 실질적인 정보(카카오 id 고유번호)를 받아옴
# 뭔가 문제가 생기면 그냥 None을 return ㅎㅎ
def kakao_callback_view(request):
    if request.method == "GET":
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
            kakao_id = profile_json.get("id")
            encrypted_kakao_id = kakao_encrypt(str(kakao_id))

            return redirect("login_for_kakao_auth", str(encrypted_kakao_id)[2:-1])

        except KeyError:
            return None
        except access_token.DoesNotExist:
            return None


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


# 카카오 ID를 정상적으로 받아왔을 때 매치 타투 로그인을 다시 요구하는 페이지
def login_for_kakao_auth_view(request, kakao_id):
    content = dict()
    # 해당 아이디로 이미 서비스 인증을 한 적이 있는가?
    already_used_kakao_id = False

    # 만약 방금 전의 카카오톡 로그인으로 입력된 계정이 인증에 사용된 계정이라면 비정상 접근
    if kakao_id in [customer.kakao_code for customer in Customer.objects.all()]:
        # 이미 인증한 사용자의 아이디를 가려서 보여줌
        authenticated_user = Customer.objects.get(kakao_code=kakao_id)
        authenticated_user_id = authenticated_user.username[:len(authenticated_user.username)//2]
        authenticated_user_id = authenticated_user_id + "..."
        print(authenticated_user_id)

        content["authenticated_id"] = authenticated_user_id
        already_used_kakao_id = True

    # 만약에 로그인한 사용자인 경우 비정상 접근임
    elif request.user.is_authenticated:
        return redirect("already_logged_in")

    else:
        if request.method == "POST":
            form = UserLoginForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request=request, username=username, password=password)

                # 카카오 아이디 갱신 / 인증 완료 체크
                user.kakao_code = kakao_id
                user.authenticated = True
                user.save()

                login(request, user)

                return redirect("auth_complete")
            else:
                return redirect("login_for_kakao_auth", kakao_id, content)

    content["form"] = UserLoginForm()
    content["already_used_kakao_id"] = already_used_kakao_id
    return render(request, "login_for_kakao_auth.html", content)


def __logout(request):
    logout(request)
    return redirect("main")


# 마이페이지
# account/mypage
@login_required(login_url="/account/login")
def mypage_view(request):
    content = dict()

    user: Customer = request.user
    user_profile_image_url = user.user_image.url
    content['user_profile_image_url'] = user_profile_image_url

    # 유저 닉네임
    nickname = user.nickname
    content['nickname'] = nickname

    # About 찜한 공고
    liked_matchings = Matching.objects.filter(author=user).order_by('-pub_date')
    # 찜한 공고 수
    liked_matchings_cnt = len(liked_matchings)
    content['liked_matchings_cnt'] = liked_matchings_cnt

    # About 작성한 리뷰
    reviews = Review.objects.filter(review_author=user).order_by('-pub_date')
    # 작성한 리뷰의 수
    review_cnt = len(reviews)
    content['review_cnt'] = review_cnt

    # About 팔로잉
    following = user.following.all()
    # 팔로우한 유저의 수
    following_cnt = len(following)
    content['following_cnt'] = following_cnt

    try:
        if request.GET['menu'] == 'review':
            content['menu'] = "review"
            # 작성한 리뷰가 없는 경우
            if review_cnt == 0:
                review_exists = False
            else:
                review_exists = True
                content['reviews'] = reviews
            content['review_exists'] = review_exists

        elif request.GET['menu'] == 'following':
            content['menu'] = "following"
            # 팔로우 중인 유저가 없는 경우
            if following_cnt == 0:
                following_exists = False
            else:
                following_exists = True
                content['following'] = following
            content['following_exists'] = following

        # 만약 GET으로 받아온 menu가 matching이면
        # + 이외의 경우
        else:
            content['menu'] = "matching"
            # 찜한 공고가 없는 경우
            if liked_matchings_cnt == 0:
                liked_matchings_exists = False
            else:
                liked_matchings_exists = True
                content['liked_matchings'] = liked_matchings
            content['liked_matchings_exists'] = liked_matchings_exists

    # 만약 GET으로 menu가 들어오지 않았다면 matching으로 간주
    except MultiValueDictKeyError:
        content['menu'] = "matching"
        # 찜한 공고가 없는 경우
        if liked_matchings_cnt == 0:
            liked_matchings_exists = False
        else:
            liked_matchings_exists = True
            content['liked_matchings'] = liked_matchings
        content['liked_matchings_exists'] = liked_matchings_exists

    return render(request, "mypage.html", content)


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
            return redirect("kakao_auth", user.username)

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
            return redirect("kakao_auth", user.username)

    else:
        form = TattooistSignUpForm()
        content["form"] = form
        content["validity_check"] = UserSignupChecker(form, default=True)
        return render(request, 'signup_tattooist.html', content)