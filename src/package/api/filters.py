from django_filters import rest_framework as filters
from package.models import *

""" Package filter """


class PackageFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    # description = filters.CharFilter(
    #     field_name='description', lookup_expr='icontains')

    class Meta:
        model = Package
        fields = '__all__'


""" School Package Filter """


class SchoolPackageFilter(filters.FilterSet):
    class Meta:
        model = SchoolPackage
        fields = '__all__'
