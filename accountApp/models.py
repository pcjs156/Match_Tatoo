from django.db import models
from django.contrib.auth.models import AbstractUser
from tools import date_upload_to




class Customer(AbstractUser): 
    class Meta:
        verbose_name = "유저"

    # tattooist: 시술자
    # customer: 피시술자
    is_tattooist = models.BooleanField("tattooist status", default=False)
    is_customer = models.BooleanField("customer status", default=False)

    # 닉네임
    nickname = models.CharField(max_length=20, blank=False, null=False, verbose_name="닉네임")

    # 사용자 대표 이미지
    user_image = models.ImageField(upload_to=date_upload_to, default="account/profile_image/user_default_image.png",
                                   blank=True, null=False, verbose_name="프로필 이미지")

    # 소개글
    introduce = models.CharField(max_length=200, blank=True, null=False, default="등록된 소개글이 없습니다." , verbose_name="소개글")
    
    # 연락처
    contact = models.CharField(max_length=50, blank=True, null=False, default="등록된 연락처가 없습니다.", verbose_name="연락처")
    
    # 가게 위치
    location = models.CharField(max_length=100, blank=True, null=True, default="등록된 위치가 없습니다.", verbose_name="위치")

    # 인증 여부
    authenticated = models.BooleanField(default=False, verbose_name="인증 여부")

    # 팔로워
    follwer = models.ManyToManyField("accountApp.Customer", blank=True, verbose_name="팔로워")

    def __str__(self):
        if self.is_tattooist:
            typeMarker = "[T]"
        elif self.is_customer:
            typeMarker = "[C]"
        else:
            typeMarker = "[U]"
        
        return typeMarker + " " + self.nickname
