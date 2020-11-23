from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


# 포트폴리오 등록 페이지
# tattooist/create_portfolio
from django.utils.datastructures import MultiValueDictKeyError

from accountApp.models import Customer
from matchingApp.models import Matching
from tattooistApp.models import Review, Portfolio


@login_required(login_url="/account/login")
def create_portfolio_view(request):
    return render(request, "create_portfolio.html")


# 리뷰 작성 뷰: in tatooist_profile.html
# 성사된 matching이 있는지 검사해야 함
# (tattooist/create_review/<tattooist_id: int>)
@login_required(login_url="/account/login")
def create_review(request, tattooist_id: int):
    pass


# 리뷰 디테일 페이지
# tattooist/detail_review/<matching_id: int>/<review_id: int>
def detail_review_view(request, review_id: int):
    return render(request, "detail_review.html")


# 포트폴리오 디테일 페이지
# tattooist/detail_portfolio/<tattooist_id: int>/<portfolio_id: int>
def detail_portfolio_view(request, tattooist_id: int, portfolio_id: int):
    return render(request, "detail_portfolio.html")


# 타투이스트와 메시지를 주고 받는 페이지
# tattooist/message/<tattooist_id: int>
@login_required(login_url="/account/login")
def message_view(request, tattooist_id: int):
    return render(request, "message.html")


# 포트폴리오를 수정하는 페이지
# 해당 포트폴리오를 작성한 사람인지 검사해야 함
# tattooist/modify_portfolio/<tattooist_id: int>/<portfolio_id: int>
@login_required(login_url="/account/login")
def modify_portfolio_view(request, tattooist_id: int, portfolio_id: int):
    return render(request, "modify_portfolio.html")


# 리뷰를 수정하는 페이지
# 해당 타투이스트에게 리뷰를 남긴 기록이 있는지 확인해야 함
# tattooist/modify_review/<tattooist_id: int>/<review_id: int>
@login_required(login_url="/account/login")
def modify_review_view(request, tattooist_id: int, review_id: int):
    return render(request, "modify_review.html")


# 개발자에게 쪽지 보내기
# tattooist/report
@login_required(login_url="/account/login")
def report_view(request):
    return render(request, "report.html")


# 타투이스트 프로필 페이지
def tattooist_profile_view(request, tattooist_id):
    content = dict()
    # 한 페이지에 노출될 썸네일의 갯수
    THUMBNAIL_PER_PAGE = 6

    # 해당 유저가 타투이스트인지 표시(타투이스트에게만 profile 페이지가 존재함)
    is_tattooist = True
    # 리뷰를 작성할 수 있는지 확인
    review_possible = False

    tattooist: Customer = get_object_or_404(Customer, pk=tattooist_id)
    content["tattooist"] = tattooist

    # 만약 해당 유저가 타투이스트가 아닌 경우
    if not tattooist.is_tattooist:
        is_tattooist = False
    # 만약 해당 유저가 타투이스트인 경우
    else:
        # 해당 프로필 페이지의 주인인가?
        is_owner = request.user.is_authenticated and tattooist == request.user
        content["is_owner"] = is_owner

        # 팔로워 수
        follower_count = tattooist.get_follower_number()

        # 리뷰를 남길 수 있는지 확인
        # 일단 로그인 한 사용자인지 확인하고,
        if request.user.is_authenticated:
            # 현재 페이지의 타투이스트가 작성한 모든 매칭을 가져옴
            matchings = Matching.objects.filter(author=tattooist)
            # 현재 대상 타투이스트가 작성한 모든 매칭에 대해
            for matching in matchings:
                # 해당 매칭이 성사되었고, 그 대상 모델이 현재 접속한 유저인 경우
                if matching.is_matched and matching.tattoo_model == request.user:
                    # 리뷰를 남길 수 있음을 표시
                    review_possible = True
                    break

        try:
            # 만약 GET으로 받아온 menu가 review이면
            if request.GET["menu"] == "review":
                # 리뷰가 가리키는 매칭의 author가 현재 대상 타투이스트인 리뷰의 목록
                reviews = Review.objects.filter(matching__author=tattooist).order_by("-pub_date")
                paginator = Paginator(reviews, THUMBNAIL_PER_PAGE)
                page = request.GET.get('page')
                products = paginator.get_page(page)
                content['reviews'] = reviews
                content["content_is_portfolio"] = False
                content["menu"] = "review"

            else:
                # 포트폴리오 목록
                portfolios = Portfolio.objects.filter(author=tattooist).order_by("-pub_date")
                paginator = Paginator(portfolios, THUMBNAIL_PER_PAGE)
                page = request.GET.get('page')
                portfolios = paginator.get_page(page)
                content['portfolios'] = portfolios
                content["content_is_portfolio"] = True
                content["menu"] = "portfolio"

        # 만약 GET으로 menu가 들어오지 않았다면 포트폴리오로 간주
        except MultiValueDictKeyError:
            # 포트폴리오 목록
            portfolios = Portfolio.objects.filter(author=tattooist).order_by("-pub_date")
            paginator = Paginator(portfolios, THUMBNAIL_PER_PAGE)
            page = request.GET.get('page')
            portfolios = paginator.get_page(page)
            content['portfolios'] = portfolios
            content["content_is_portfolio"] = True
            content["menu"] = "portfolio"

    content["is_tattooist"] = is_tattooist
    content["follower_count"] = follower_count
    content["review_possible"] = review_possible

    return render(request, "tattooist_profile.html", content)