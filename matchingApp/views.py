from datetime import datetime

from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accountApp.models import Customer
from .models import Matching
from .forms import MatchingForm

from tools import reversed_dict, parse_dict_from_code_pair
from .tools import searching_keyword_validation


# matching 디테일 페이지
# matching/detail_matching/<tattooist_id: int>/<matching_id: int>
def detail_matching_view(request, tattooist_id: int, matching_id: int):
    content = dict()

    tattooist = Customer.objects.get(id=tattooist_id)
    content["tattooist"] = tattooist

    matching = Matching.objects.get(pk=matching_id)
    content["matching"] = matching

    is_author = request.user.is_authenticated and request.user.id == tattooist_id
    content["is_author"] = is_author

    return render(request, "detail_matching.html", content)


# customer가 tattooist만 접근 가능한 기능에 접근하는 경우
def customer_request_rejected_view(request):
    return render(request, "customer_request_rejected.html")


# 조건에 맞는 matching의 리스트를 pagination으로 보여주는 페이지
# matching/matching_list?region=인천&type=미니타투&part=목&order-by=price(또는 pub-date)
def matching_list_view(request):
    content = dict()
    content["is_tattooist"] = (request.user.is_authenticated) and (request.user.is_tattooist)

    try:
        region = request.GET["region"]     # 지역
        tattoo_type = request.GET["type"]  # 타투 유형
        part = request.GET["part"]         # 타투 부위
        orderby = request.GET["order-by"]  # 정렬 방법(price/description)

        # GET으로 받아온 매칭 검색 조건이 유효한지 검사
        keyword_validation = searching_keyword_validation(region=region,
                                                          tattoo_type=tattoo_type,
                                                          part=part,
                                                          orderby=orderby)
        # 검색 조건의 유효성을 확인해 유효한 조건으로만 필터링
        if not keyword_validation["region"]:
            # 맨 처음 조건(지역)이 유효하지 않다면 필터링을 거치지 않으므로 전부 가져옴
            result_matching_list = Matching.objects.all()
        else:
            code_value_dict = parse_dict_from_code_pair(Matching.REGION)
            region_code = reversed_dict(code_value_dict)[region]
            result_matching_list = Matching.objects.filter(region=region_code)

        if keyword_validation["tattoo_type"]:
            code_value_dict = parse_dict_from_code_pair(Matching.TYPE)
            tattoo_type_code = reversed_dict(code_value_dict)[tattoo_type]
            result_matching_list = result_matching_list.filter(tattoo_type=tattoo_type_code)

        if keyword_validation["part"]:
            code_value_dict = parse_dict_from_code_pair(Matching.PART)
            part_code = reversed_dict(code_value_dict)[part]
            result_matching_list = result_matching_list.filter(part=part_code)

        if keyword_validation["order-by"]:
            if orderby == "price":
                result_matching_list = result_matching_list.order_by("price")
            elif orderby == "pub-date":
                result_matching_list = result_matching_list.order_by("-pub_date")
        # 정렬 순서가 유효하지 않은 경우 최신순으로 정렬
        else:
            result_matching_list = result_matching_list.order_by('-pub_date')


    # 검색 조건 중 하나라도 입력되지 않은 경우 매칭 전체를 최신순으로 보여줌
    except MultiValueDictKeyError:
        result_matching_list = Matching.objects.order_by("-pub_date")


    content["result_matching_list"] = result_matching_list.filter(is_matched=False)
    return render(request, "matching_list.html", content)


# 매칭 작성 페이지
# tattooist만 접근 가능해야 함
# matching/create_matching
@login_required(login_url="/account/login")
def create_matching_view(request):
    # 로그인 하지 않았거나, 타투이스트가 아닌 사용자가 접근할 경우
    if not request.user.is_authenticated or not request.user.is_tattooist:
        return redirect("customer_request_rejected")

    content = dict()
    content["error"] = False

    if request.method == "POST":
        form = MatchingForm(request.POST)

        if form.is_valid() and request.POST["region"] != "R0":
            matching: Matching = form.save(commit=False)
            matching.author = request.user
            matching.save()
            print(matching.region)
            return redirect("matching_list")
        else:
            content["error"] = True
            content["form"] = form
            return render(request, "create_matching.html", content)

    else:
        form = MatchingForm()
        content["form"] = form
        return render(request, "create_matching.html", content)


# matching 수정 페이지
# 해당 matching의 작성자인지 확인해야 함
# matching/modify_matching/<tattooist_id: int>/<matching_id: int>
@login_required(login_url="/account/login")
def modify_matching_view(request, tattooist_id: int, matching_id: int):
    matching = Matching.objects.get(pk=matching_id)

    # 만약 로그인하지 않았거나, 작성자가 아닌 경우
    if not request.user.is_authenticated or request.user.id != matching.author.id:
        return redirect("customer_request_rejected")

    content = dict()
    content["error"] = False

    if request.method == "POST":
        form = MatchingForm(request.POST)

        if form.is_valid() and request.POST["region"] != "R0":
            updated_matching = form.save(commit=False)

            matching.title = updated_matching.title
            matching.region = updated_matching.region
            matching.region_detail = updated_matching.region_detail
            matching.tattoo_type = updated_matching.tattoo_type
            matching.part = updated_matching.part
            matching.price = updated_matching.price
            matching.description = updated_matching.description
            matching.pub_date = datetime.now()

            matching.save()

            return redirect("detail_matching", tattooist_id, matching_id)
        else:
            content["error"] = True
            content["form"] = form
            print(form)
            return render(request, "modify_matching.html", content)

    else:
        form = MatchingForm(instance=matching)
        content["form"] = form
        return render(request, "modify_matching.html", content)