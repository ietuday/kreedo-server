from period.models import*
from django_filters import rest_framework as filters


""" Period Template Filter """


class PeriodTemplateFilter(filters.FilterSet):
    class Meta:
        model = PeriodTemplate
        fields = '__all__'


""" Period Filter """


class PeriodFilter(filters.FilterSet):
    class Meta:
        model = Period
        fields = '__all__'


""" Period Template Detail Filter """


class PeriodTemplateDetailFilter(filters.FilterSet):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
