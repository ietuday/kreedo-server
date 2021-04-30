from django_filters import rest_framework as filters
from django_filters import DateRangeFilter, DateFilter
from session.models import*


""" SchoolSession Filter """


class SchoolSessionFilter(filters.FilterSet):

    class Meta:
        model = SchoolSession
        fields = '__all__'


""" AcademicSession Filter """


class AcademicSessionFilter(filters.FilterSet):
    class Meta:
        model = AcademicSession
        fields = '__all__'


""" AcademicCalender Filter """


class AcademicCalenderFilter(filters.FilterSet):
    class Meta:
        model = AcademicCalender
        fields = '__all__'
