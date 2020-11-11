from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Matching
from tools import reversed_dict, parse_dict_from_code_pair
from .tools import searching_keyword_validation

# matching 디테일 페이지
# matching/detail_matching/<tattooist_id: int>/<matching_id: int>
def detail_matching_view(request, tatooist_id: int, matching_id: int):
    return render(request, "detail_matching.html")


# 조건에 맞는 matching의 리스트를 pagination으로 보여주는 페이지
# matching/matching_list?region=인천&type=미니타투&part=목&order-by=price(또는 pub-date)
def matching_list_view(request):
    content = dict()

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
    return render(request, "create_matching.html")


# matching 수정 페이지
# 해당 matching의 작성자인지 확인해야 함
# matching/modify_matching/<tattooist_id: int>/<matching_id: int>
@login_required(login_url="/account/login")
def modify_matching_view(request, tattooist_id: int, matching_id: int):
    return render(request, "modify_mathching.html")