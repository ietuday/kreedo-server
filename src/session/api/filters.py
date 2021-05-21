from django_filters import rest_framework as filters
from django_filters import DateRangeFilter, DateFilter
from session.models import*


""" SchoolSession Filter """


class SchoolSessionFilter(filters.FilterSet):
    school_name = filters.CharFilter(
        field_name='school__name', lookup_expr='icontains')

    class Meta:
        model = SchoolSession
        fields = '__all__'


""" SchoolCalendar Filter """


class SchoolCalendarFilter(filters.FilterSet):
    school_name = filters.CharFilter(
        field_name='school__name', lookup_expr='icontains')

    class Meta:
        model = SchoolCalendar
        fields = '__all__'


""" AcademicCalender Filter """


class AcademicCalenderFilter(filters.FilterSet):
    class Meta:
        model = AcademicCalender
        fields = '__all__'


""" AcademicSession Filter """


class AcademicSessionFilter(filters.FilterSet):
    school_session = filters.CharFilter(
        field_name='school__name', lookup_expr='icontains')

    class Meta:
        model = AcademicSession
        fields = '__all__'
