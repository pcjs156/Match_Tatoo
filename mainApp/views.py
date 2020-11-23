from django.shortcuts import render

from matchingApp.models import Matching

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

    # 최신 매칭 목록
    latest_matchings = Matching.objects.all().order_by('-pub_date')[:MATCHING_NUMBER]
    content["latest_matchings"] = latest_matchings

    # 인기 매칭 목록
    popular_matchings = [matching for matching in Matching.objects.all()]
    popular_matchings.sort(key=lambda matching: len(matching.likers.all()), reverse=True) # likers의 길이에 맞춰 정렬
    popular_matchings = popular_matchings[:MATCHING_NUMBER]
    content["popular_matchings"] = popular_matchings

    return render(request, "main.html", content)