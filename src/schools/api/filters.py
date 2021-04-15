from ..models import*
from django_filters import rest_framework as filters


""" Grade filter """
class GradeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = Grade
        fields = '__all__'

""" Section Filter """
class SectionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = Section
        fields = '__all__'
    
""" Subject filter"""
class SubjectFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = Subject
        fields ='__all__'


""" License Filter"""
class LicenseFilter(filters.FilterSet):
    class Meta:
        model = License
        fields = '__all__'

""" School Filter"""
class SchoolFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = School
        fields = '__all__'