import django_filters
from django import forms
from .models import *

choices = {
    ('Cheap', 'cheap'),
    ('Expensive', 'expensive'),
}

time_choice = {
    ('New', 'new'),
    ('Old', 'old'),
}

like_choice = {
    ('Like', 'like'),
    ('Like_', 'like_'),
}


class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    price_sort = django_filters.ChoiceFilter(choices=choices, method='price_method')
    time_sort = django_filters.ChoiceFilter(choices=time_choice, method='time_method')
    like_sort = django_filters.ChoiceFilter(choices=like_choice, method='like_method')

    def price_method(self, queryset, name, value):
        data = 'unit_price' if value == 'Cheap' else '-unit_price'
        return queryset.order_by(data)

    def time_method(self, queryset, name, value):
        data = 'create' if value == 'Old' else '-create'
        return queryset.order_by(data)

    def like_method(self, queryset, name, value):
        data = 'total_like' if value == 'Like' else '-total_like'
        return queryset.order_by(data)
