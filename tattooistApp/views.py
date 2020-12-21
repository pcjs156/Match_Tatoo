from datetime import datetime

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError

from accountApp.models import Customer
from mainApp.models import Report
from matchingApp.models import Matching
from tattooistApp.models import Review, Portfolio
from mainApp.forms import ReportForm

from .forms import PortfolioForm, MessageForm

# 포트폴리오 등록 페이지
# tattooist만 접근 가능해야 함
# tattooist/create_portfolio
@login_required(login_url="/account/login")
def create_portfolio_view(request):
    # 로그인 하지 않았거나, 타투이스트가 아닌 사용자가 접근할 경우
    if not request.user.is_authenticated or not request.user.is_tattooist:
        return HttpResponse('유효하지 않은 접근입니다.')

    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES)

        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.author = request.user
            portfolio.save()
            return redirect("tattooist_profile", request.user.id)
        else:
            return HttpResponse('It is not valid')

    else:
        form = PortfolioForm()
        return render(request, "create_portfolio.html", {'form':form})


# 리뷰 작성 뷰: in tatooist_profile.html
# 성사된 matching이 있는지 검사해야 함
# (tattooist/create_review/<tattooist_id: int>)
@login_required(login_url="/account/login")
def create_review(request, tattooist_id: int):
    pass


@login_required(login_url="/account/login")
def delete_portfolio(request, portfolio_id: int):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    author = portfolio.author

    # 만약 로그인하지 않았거나, 작성자가 아닌 경우
    if not request.user.is_authenticated or request.user.id != portfolio.author.id:
        return redirect("customer_request_rejected")

    portfolio.delete()

    return redirect("tattooist_profile", author.id)


# 리뷰 디테일 페이지
# tattooist/detail_review/<matching_id: int>/<review_id: int>
def detail_review_view(request, review_id: int):
    content = dict()

    review = Review.objects.get(pk=review_id)
    content['review'] = review

    tattooist = review.matching.author
    content['tattooist'] = tattooist

    # 현재 화면을 보고 있는 유저가 해당 리뷰의 대상 매칭의 작성자인 경우
    if request.user.is_authenticated and tattooist == request.user:
        is_author = True
    else:
        is_author = False
    content['is_author'] = is_author

    # 현재 화면을 보고 있는 유저가 로그인해 있고, 타투이스트를 팔로우 하고 있는 경우
    if request.user.is_authenticated and tattooist in request.user.following.all():
        now_following = True
    else:
        now_following = False
    content['now_following'] = now_following

    follower_count = tattooist.get_follower_number()
    content['follower_count'] = follower_count

    return render(request, "detail_review.html", content)


# 포트폴리오 디테일 페이지
# tattooist/detail_portfolio/<tattooist_id: int>/<portfolio_id: int>
def detail_portfolio_view(request, tattooist_id: int, portfolio_id: int):
    content = dict()

    tattooist = Customer.objects.get(id=tattooist_id)
    content["tattooist"] = tattooist

    is_author = request.user.is_authenticated and request.user == tattooist
    content['is_author'] = is_author

    portfolio = Portfolio.objects.get(pk=portfolio_id)
    content["portfolio"] = portfolio

    return render(request, "detail_portfolio.html", content)


# 팔로우 버튼이 눌린 경우 해당 유저가 로그인 되어 있는지 먼저 검사하고
# 만약 로그인했을 경우, 팔로우를 누르지 않았다면 팔로우, 팔로우를 눌렀다면 팔로우 해제
@login_required(login_url="/account/login")
def follow_pressed(request, tattooist_id):
    # 대상 타투이스트
    tattooist: Customer = Customer.objects.get(pk=tattooist_id)
    # 나
    me: Customer = request.user

    # 만약 팔로우를 누르지 않았다면 팔로우
    if tattooist not in me.following.all():
        me.following.add(tattooist)
        me.save()
    # 만약 팔로우를 눌렀다면 팔로우 해제
    else:
        me.following.remove(tattooist)
        me.save()

    return redirect("tattooist_profile", tattooist_id)

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
    portfolio = Portfolio.objects.get(pk=portfolio_id)

    # 만약 로그인하지 않았거나, 작성자가 아닌 경우
    if not request.user.is_authenticated or request.user.id != portfolio.author.id:
        return HttpResponse('유효하지 않은 접근입니다.')

    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES)

        if form.is_valid():
            updated_portfolio = form.save(commit=False)

            portfolio.author = updated_portfolio.author
            portfolio.portfolio_image = updated_portfolio.portfolio_image
            portfolio.pub_date = datetime.now()
            portfolio.description = updated_portfolio.description

            portfolio.save()
            return redirect("detail_portfolio", tattooist_id, portfolio_id)
        else:
            return render(request, "modify_portfolio.html", {'form':form})

    else:
        form = PortfolioForm(instance=portfolio)
        return render(request, "modify_portfolio.html", {'form':form})


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
    content = dict()

    if request.method == "POST":
        form = ReportForm(request.POST)

        if form.is_valid():
            report: Report = form.save(commit=False)
            report.customer = request.user
            report.save()

        return redirect("main")

    else:
        form = ReportForm()
        content["form"] = form

        return render(request, "report.html", content)


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

    # 현재 화면을 보고 있는 유저가 로그인해 있고, 타투이스트를 팔로우 하고 있는 경우
    if request.user.is_authenticated and tattooist in request.user.following.all():
        now_following = True
    else:
        now_following = False
    content['now_following'] = now_following

    # 팔로워 수
    follower_count = tattooist.get_follower_number()
    content["follower_count"] = follower_count

    # 만약 해당 유저가 타투이스트가 아닌 경우
    if not tattooist.is_tattooist:
        is_tattooist = False
    # 만약 해당 유저가 타투이스트인 경우
    else:
        # 해당 프로필 페이지의 주인인가?
        is_owner = request.user.is_authenticated and tattooist == request.user
        content["is_owner"] = is_owner

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
    content["review_possible"] = review_possible

    return render(request, "tattooist_profile.html", content)