from django.contrib import admin
from .models import Portfolio, Review, Message

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Review)
admin.site.register(Message)