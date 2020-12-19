from django.shortcuts import render

from accountApp.models import Customer
from matchingApp.models import Matching
from django.db.models import Q

from django.core.paginator import Paginator
import math

# 인트로 페이지
# /
def intro_view(request):
    return render(request, "intro.html")

# 메인 페이지
# /main
def main_view(request):
    content = dict()

    # main 페이지로 전달될 목록당 매칭의 수
    MATCHING_NUMBER = 4
    # main 페이지로 전달될 목록당 타투이스트의 수
    TATTOOIST_NUMBER = 4

    # 최신 매칭 목록
    latest_matchings = Matching.objects.all().order_by('-pub_date')[:MATCHING_NUMBER]
    content["latest_matchings"] = latest_matchings

    # 인기 매칭 목록
    popular_matchings = [matching for matching in Matching.objects.all()]
    popular_matchings.sort(key=lambda matching: len(matching.likers.all()), reverse=True) # likers의 길이에 맞춰 정렬
    popular_matchings = popular_matchings[:MATCHING_NUMBER]
    content["popular_matchings"] = popular_matchings

    # 타투이스트 목록: 타투이스트이며, 인증된 타투이스트만 먼저 골라옴
    tattooists = Customer.objects.filter(is_tattooist=True, authenticated=True)

    # 신규 타투이스트 목록
    new_tattooists = tattooists.order_by('-date_joined')[:TATTOOIST_NUMBER]
    content["new_tattooists"] = new_tattooists

    # 인기 타투이스트 목록
    popular_tattooists = sorted(list(tattooists), key=lambda tattooist: len(tattooist.following.all()), reverse=True)[:TATTOOIST_NUMBER]
    content["popular_tattooists"] = popular_tattooists
    
    # 성사되지 않은 매칭의 갯수
    total_unmatched_matching_cnt = len(Matching.objects.all().filter(is_matched=False))
    print(total_unmatched_matching_cnt)
    content["total_unmatched_matching_cnt"] = total_unmatched_matching_cnt

    return render(request, "main.html", content)

# 검색결과 페이지
# /search_result
def search_result_view(request):
    content = dict()
    
    w = request.GET.get('w') or ""
    content["w"] = w

    search_result = Matching.objects.filter(
        Q(title__icontains=w) | Q(tattoo_type__icontains=w) |
        Q(description__icontains=w) | Q(part__icontains=w)
    ).distinct()  # 중복사항 제거
    content["search_result"] = search_result

    paginator = Paginator(search_result, 2)
    page = request.GET.get('page')
    post_counts = paginator.get_page(page)
    content["post_counts"] = post_counts

    if w == "":   # w가 작성되지 않았을 경우, search_result 비우기
        del(content["search_result"])
    if page == "" or page == None:
        page = 1
    
    page_range = 5 # 보여질 페이지 범위 지정
    current_block = math.ceil(int(page)/page_range)
    start_block = (current_block-1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    content["p_range"] = p_range

    return render(request, "search_result.html", content)