import os
from uuid import uuid4
from django.utils import timezone

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from matchingApp.models import Customer, Matching

from tools import date_upload_to

class Portfolio(models.Model):
    class Meta:
        verbose_name = "포트폴리오"
    
    # 포트폴리오 작성자
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=False, related_name="portfolio_author", verbose_name="포트폴리오 작성자")
    
    # 사진
    portfolio_image = models.ImageField(upload_to=date_upload_to, blank=False, null=False, verbose_name="포트폴리오 사진")

    # 작성일
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    # 본문
    description = models.TextField(null=False, blank=True, default="",verbose_name="포트폴리오 본문")

    def __str__(self):
        if len(self.description) > 10:
            body = self.description[:10] + "..."
        else:
            body = self.description[:]
        return f"[{self.author.nickname}, on {self.pub_date}] " + body


class Review(models.Model):
    class Meta:
        verbose_name = "리뷰"
    
    # 대상 매칭
    matching = models.ForeignKey(Matching, on_delete=models.SET_NULL, blank=True, null=True, related_name="review_matching", verbose_name="대상 매칭")

    # 작성자
    review_author = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="matching_review_autor", verbose_name="리뷰 작성자")
    
    # 작성 일자
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    
    # 별점
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5, verbose_name="별점")

    # 사진
    review_image = models.ImageField(upload_to=date_upload_to, default="tattoistApp/review_image/default_review_image.png", blank=True, null=False, verbose_name="리뷰 사진")

    # 본문
    description = models.TextField(null=False, blank=True, default="",verbose_name="리뷰 본문")
    
    def __str__(self):
        if len(self.description) > 10:
            body = self.description[:10] + "..."
        else:
            body = self.description[:]
        return f"[{self.review_author.nickname}, on {self.pub_date}] " + body


class Message(models.Model):
    class Meta:
        verbose_name = "메시지"
    
    # 수신자: tattooist
    tattooist = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="message_tattooist", verbose_name="메세지 수신자")
    
    # 발신자: customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="message_customer", verbose_name="메세지 발신자")
    
    # 발송 일자
    send_datetime = models.DateTimeField(auto_now_add=True, verbose_name="전송 일/시간")
    
    #본문
    description = models.TextField(null=False, blank=True, default="",verbose_name="메세지 본문")
    
    def __str__(self):
        if len(self.description) > 10:
            body = self.description[:10] + "..."
        else:
            body = self.description[:]
        return f"[{self.tattooist}, on {self.send_datetime}] " + body