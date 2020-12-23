from django import template
from matchingApp.models import Matching
from accountApp.models import Customer
from tattooistApp.models import Review

register = template.Library()


# message.html 에서 메세지의 이후 객체를 가져오기 위한 필터
@register.filter
def next(some_list, current_index):
    try:
        return some_list[int(current_index) + 1]
    except:
        return ''


# message.html 에서 메세지의 이전 객체를 가져오기 위한 필터
@register.filter
def previous(some_list, current_index):
    try:
        return some_list[int(current_index) - 1]
    except:
        return ''


# create_review.html 에서 타투이스트 - 사용자간의 성사된 매칭만을 가져오기 위한 태그
@register.simple_tag
def get_matchings(tattooist_id, user_id):
    try:
        tattooist: Customer = Customer.objects.get(pk=tattooist_id)
        user: Customer = Customer.objects.get(pk=user_id)
        
        return Matching.objects.filter(author=tattooist, tattoo_model=user, is_matched=True)
    except:
        return ''


# modify_review.html 에서 리뷰의 이미지를 가져오기 위한 태그
@register.simple_tag
def get_image(review_id):
    try:
        return Review.objects.get(pk=review_id).review_image.url
    except:
        return ''



    
    

