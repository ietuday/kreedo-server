from django_filters import rest_framework as filters
from django_filters import DateRangeFilter, DateFilter
from holiday.models import*

""" School holioday Filter """


class SchoolHolidayFilter(filters.FilterSet):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'


"""School waek Off Filter """


class SchoolWeakOffFilter(filters.FilterSet):
    class Meta:
        model = SchoolWeakOff
        fields = '__all__'
