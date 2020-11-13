from django import forms

from .models import Matching

class MatchingForm(forms.ModelForm):
    class Meta:
        model = Matching
        fields = ['title', 'region', 'region_detail', 'price', 'tattoo_type', 'part', 'description']
