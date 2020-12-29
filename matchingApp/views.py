from datetime import datetime

from django.core.paginator import Paginator
from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accountApp.models import Customer
from .models import Matching
from .forms import MatchingForm

from tools import reversed_dict, parse_dict_from_code_pair, tuple_pair_to_dict
from .tools import searching_keyword_validation


# matching 디테일 페이지
# matching/detail_matching/<tattooist_id: int>/<matching_id: int>
def detail_matching_view(request, tattooist_id: int, matching_id: int):
    content = dict()

    tattooist = Customer.objects.get(id=tattooist_id)
    content["tattooist"] = tattooist

    matching = Matching.objects.get(pk=matching_id)
    content["matching"] = matching

    # 해당 matching의 작성자인지 표시
    is_author = request.user.is_authenticated and request.user.id == tattooist_id
    content["is_author"] = is_author

    likers = [customer.nickname for customer in matching.likers.all()]
    if len(likers) == 0:
        like_message = "아직 찜 되지 않았습니다."
    else:
        like_message = f"{len(likers)}명의 유저가 해당 매칭을 찜 하셨습니다."
    content["like_message"] = like_message

    # 현재 유저가 해당 게시물을 찜했는지 확인
    user_like = False
    if request.user.is_authenticated:
        user_like = matching.likers.filter(username=request.user.username).exists()
    content["user_like"] = user_like

    return render(request, "detail_matching.html", content)


# matching 삭제
# 해당 matching의 작성자인지 확인해야 함
# matching/delete_matching/<tattooist_id: int>/<matching_id: int>
def delete_matching(request, tattooist_id: int, matching_id: int):
    matching = Matching.objects.get(pk=matching_id)

    # 만약 로그인하지 않았거나, 작성자가 아닌 경우
    if not request.user.is_authenticated or request.user.id != matching.author.id:
        return redirect("customer_request_rejected")

    matching.delete()

    return redirect("matching_list")

# customer가 tattooist만 접근 가능한 기능에 접근하는 경우
def customer_request_rejected_view(request):
    return render(request, "customer_request_rejected.html")


# 조건에 맞는 matching의 리스트를 pagination으로 보여주는 페이지
# matching/matching_list?region=인천&type=미니타투&part=목&order-by=price(또는 pub-date)
def matching_list_view(request):
    content = dict()
    content["is_tattooist"] = (request.user.is_authenticated) and (request.user.is_tattooist)

    region_now = "전체"
    tattoo_type_now = "전체"
    part_now = "전체"
    orderby_now = "최신순"

    # GET으로 조건을 받아올 때 정해지지 않은 입력값이 들어온 경우 경고 메시지를 띄우기 위한 변수
    unmatched_condition = False

    try:
        region = request.GET["region"]     # 지역
        tattoo_type = request.GET["tattoo_type"]  # 타투 유형
        part = request.GET["part"]         # 타투 부위
        orderby = request.GET["order-by"]  # 정렬 방법(price/pub_date)


        region_code = reversed_dict(tuple_pair_to_dict(Matching.REGION))[region]
        if region in [pair[1] for pair in Matching.REGION] and region != "전체":
            result_matching_list = Matching.objects.filter(region=region_code, is_matched=False)
            region_now = region
        else:
            result_matching_list = Matching.objects.filter(is_matched=False)
            unmatched_condition = True

        tattoo_type_code = reversed_dict(tuple_pair_to_dict(Matching.TYPE))[tattoo_type]
        if tattoo_type in [pair[1] for pair in Matching.TYPE] and tattoo_type != "전체":
            result_matching_list = result_matching_list.filter(tattoo_type=tattoo_type_code)
            tattoo_type_now = tattoo_type
        else:
            unmatched_condition = True

        part_code = reversed_dict(tuple_pair_to_dict(Matching.PART))[part]
        if part in [pair[1] for pair in Matching.PART] and part != "전체":
            result_matching_list = result_matching_list.filter(part=part_code)
            part_now = part
        else:
            unmatched_condition = True

        if orderby in ("pub_date", "price"):
            orderby = "price" if orderby=="price" else "-pub_date"
            result_matching_list = result_matching_list.order_by(orderby)
            orderby_now = "가격순" if orderby=="price" else "최신순"
        else:
            result_matching_list = result_matching_list.order_by("-pub_date")
            unmatched_condition = True

    # 검색 조건 중 하나라도 입력되지 않은 경우 성사되지 않은 매칭 전체를 최신순으로 보여줌
    except MultiValueDictKeyError:
        result_matching_list = Matching.objects.filter(is_matched=False).order_by("-pub_date")

    # 페이지네이션
    paginator = Paginator(result_matching_list, 9)
    try:
        page = request.GET.get('page')
    except MultiValueDictKeyError:
        page = 1
    result_matching_list = paginator.get_page(page)

    content["unmatched_condition"] = unmatched_condition
    content["region_now"] = region_now
    content["tattoo_type_now"] = tattoo_type_now
    content["part_now"] = part_now
    content["orderby_now"] = orderby_now

    content["result_matching_list"] = result_matching_list
    return render(request, "matching_list.html", content)

# 매칭 찜 버튼이 눌린 경우 해당 유저가 로그인 되어 있는지 먼저 검사하고
# 만약 로그인했을 경우, 찜을 누르지 않았다면 찜 표시, 찜을 눌렀다면 찜 해제
@login_required(login_url="/account/login")
def matching_like_pressed(request, matching_id):
    # 대상 매칭
    matching = Matching.objects.get(pk=matching_id)

    # 만약 찜을 누르지 않았다면 찜 표시
    if not matching.likers.filter(username=request.user.username).exists():
        matching.likers.add(request.user)
        matching.save()
    # 만약 찜을 눌렀다면 찜 해제
    else:
        matching.likers.remove(request.user)
        matching.save()

    matching_author_id = matching.author.id
    return redirect("detail_matching", matching_author_id, matching_id)

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
        form = MatchingForm(request.POST, request.FILES)

        if form.is_valid() and request.POST["region"] != "R0":
            matching: Matching = form.save(commit=False)
            matching.author = request.user
            matching.save()
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
        form = MatchingForm(request.POST, request.FILES)

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

            try:
                updated_image = request.FILES["image"]
            # 이미지가 변경되지 않을 경우 기존 이미지를 그대로 사용
            except MultiValueDictKeyError:
                pass
            else:
                matching.image = updated_image

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
        content["image_url"] = matching.image.url
        return render(request, "modify_matching.html", content)