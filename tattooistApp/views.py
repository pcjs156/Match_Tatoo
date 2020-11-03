from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# 포트폴리오 등록 페이지
# tattooist/create_portfolio
@login_required(login_url="/account/login")
def create_portfolio_view(request):
    return render(request, "create_portfolio.html")


# 리뷰 작성 뷰: in tatooist_profile.html
# 성사된 matching이 있는지 검사해야 함
# (tattooist/create_review/<tattooist_id: int>)
@login_required(login_url="/account/login")
def create_review(request, tattooist_id: int):
    pass


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