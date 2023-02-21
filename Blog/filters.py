import django_filters
from .models import *
from django_filters import DateFilter, RangeFilter, DateFromToRangeFilter
from django import forms
from django_filters.widgets import RangeWidget




class PostFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="creation_date", lookup_expr="gte",)
    date_range = DateFromToRangeFilter(field_name="creation_date", widget=RangeWidget(attrs={'placeholder': 'MM/DD/RRRR', 'class': 'form-control'}))
    
    class Meta:
        model = Post
        fields = ['title','published',]
        
        

