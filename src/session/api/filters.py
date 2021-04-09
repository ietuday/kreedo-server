from django_filters import rest_framework as filters
from django_filters import DateRangeFilter, DateFilter
from session.models import*


class SchoolSessionFilter(filters.FilterSet):
    # year = DateRangeFilter(field_name='year')
    # session_from = DateRangeFilter(field_name='session_from')
    # session_till = DateRangeFilter(field_name='session_till')

    class Meta:
        model = SchoolSession
        fields = '__all__'


# class AcademicSessionFilter(filters.Filter):
#     class Meta:
#         model = AcademicSession
#         fields = '__all__'
