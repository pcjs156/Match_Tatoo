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
    # 암호화된 카카오톡 고유 ID
    kakao_code = models.CharField(max_length=80, blank=True, null=True, verbose_name="카카오톡 고유 ID")

    # 팔로잉
    following = models.ManyToManyField("accountApp.Customer", blank=True, verbose_name="팔로잉")

    # 이메일 수신 동의
    mailing_agreement = models.BooleanField(default=False, verbose_name="이메일 수신 동의")

    def __str__(self):
        if self.is_tattooist:
            typeMarker = "[T]"
        elif self.is_customer:
            typeMarker = "[C]"
        else:
            typeMarker = "[U]"
        
        return typeMarker + f" ({self.id}) " + self.nickname

    def get_follower_number(self):
        following_count = 0
        users = Customer.objects.all()

        for user in users:
            if self in user.following.all():
                following_count += 1

        if following_count >= 1000:
            following_count = "%.1f" % (following_count/1000) + "K"

        return following_count

    def get_short_introduce(self):
        return self.introduce if len(self.introduce) < 20 else self.introduce[:17] + "..."