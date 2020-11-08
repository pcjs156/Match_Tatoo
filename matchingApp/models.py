from django.db import models
from accountApp.models import Customer

# 매칭 게시글
class Matching(models.Model): 
    class Meta:
        verbose_name = "매칭 게시글"

    # 매칭 작성자
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=False, related_name="matching_author_tattooist", verbose_name="매칭 작성자")

    # 타투 모델
    tattoo_model = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="matching_tatoo_model", verbose_name="타투 모델")

    # 성사 여부
    is_matched = models.BooleanField(default=False, verbose_name="성사 여부")

    # 지역
    __RAW_REGION_STRING = "지역 서울특별시 부산광역시 대구광역시 "\
                        + "인천광역시 광주광역시 울산광역시 "\
                        + "세종특별자치시 경기도 강원도 충청북도 "\
                        + "충청남도 경상북도 경상남도 제주특별자치도"
    REGION = tuple((f"R{code}", name) for code, name in enumerate(__RAW_REGION_STRING.split()))
    region = models.CharField(max_length=8, default=("R0", "지역"), blank=False, null=False, choices=REGION, verbose_name="지역")

    # 지역 상세
    region_detail = models.CharField(max_length=30, default="", blank=False, null=False, verbose_name="지역 상세 정보")

    # 타투 유형
    __RAW_TYPE_STRING =  "기타 이레즈미 블랙앤그레이 올드스쿨 "\
                       + "뉴스쿨 뉴재패니즈투 레터링 "\
                       + "인물타투 라인워크 미니타투 "
    TYPE = tuple((f"T{code}", name) for code, name in enumerate(__RAW_TYPE_STRING.split()))
    tattoo_type = models.CharField(max_length=20, default=("T0", "기타"), blank=False, null=False, choices=TYPE, verbose_name="타투 유형")

    # 부위
    __RAW_PART_STRING = "기타 머리 쇄골 목 어깨 "\
                       + "가슴 명치 옆구리 배 "\
                       + "윗팔등 팔등 팔꿈치 "\
                       + "손등 손날 손가락 "\
                       + "무릎 허벅지 종아리 발등 "
    PART = tuple((f"P{code}", name) for code, name in enumerate(__RAW_PART_STRING.split()))
    part = models.CharField(max_length=20, default=("P0", "기타"), blank=False, null=False, choices=PART ,verbose_name="부위")

    # 가격
    price = models.PositiveIntegerField(null=False, blank = False, verbose_name="가격")
    
    # 설명
    description = models.TextField(null=False, blank=True, default="",verbose_name="공고글")

    # 작성일
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    def __str__(self):
        return f"[{self.author} - {self.tattoo_model} - {self.pub_date}]"

