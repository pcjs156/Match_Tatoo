from django import forms

from .models import Portfolio, Message, Review

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['portfolio_image','description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['score', 'review_image', 'description']