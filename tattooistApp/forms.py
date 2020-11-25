from django import forms

from .models import Portfolio, Message

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['portfolio_image','description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['tattooist', 'customer','description']