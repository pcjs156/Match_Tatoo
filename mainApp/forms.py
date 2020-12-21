from django import forms

from .models import Report


class SearchForm(forms.Form):
    search_word = forms.CharField(label='search_word')


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['description']