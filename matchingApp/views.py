from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# matching 디테일 페이지
# matching/detail_matching/<tattooist_id: int>/<matching_id: int>
def detail_matching_view(request, tatooist_id: int, matching_id: int):
    return render(request, "detail_matching.html")


# 조건에 맞는 matching의 리스트를 pagination으로 보여주는 페이지
# matching/matching_list
def matching_list_view(request):
    return render(request, "matching_list.html")


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