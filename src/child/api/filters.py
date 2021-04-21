from django_filters import rest_framework as filters
from child.models import*

""" Child Filter """


class ChildFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(
        field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = 'Child'
        fields = '__all__'


class ChildDetailFilter(filters.FilterSet):
    class Meta:
        model = 'ChildDetail'
        fields = '__all__'
