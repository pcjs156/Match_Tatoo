from django.db import models
from accountApp.models import Customer

class Report(models.Model):
    class Meta:
        verbose_name = "문의"
    
    # 문의자
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="report_user", verbose_name="문의자")
    
    # 발송 일자
    send_datetime = models.DateTimeField(auto_now_add=True, verbose_name="전송 일/시간")
    
    # 본문
    description = models.TextField(null=False, blank=True, default="",verbose_name="문의 본문")

    # 확인한 문의 내역인가?
    is_checked = models.BooleanField(default=False, verbose_name="확인 여부")

    def __str__(self):
        if len(self.description) > 10:
            body = self.description[:10] + "..."
        else:
            body = self.description[:]
        print(f"[{self.customer.nickname}, on {self.send_datetime}] " + body)
        return f"[{self.customer.nickname}, on {self.send_datetime}] " + body