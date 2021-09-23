from period.models import*
from django_filters import rest_framework as filters


""" Period Template Filter """


class PeriodTemplateFilter(filters.FilterSet):
    name= filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    class Meta:
        model = PeriodTemplate
        fields = '__all__'


""" Period Filter """


class PeriodFilter(filters.FilterSet):
    # subject = filters.CharFilter(
    #     field_name='subject__name', lookup_expr='icontains')

    # class Meta:
    #     model = Period
    #     fields = '__all__'
    pass


""" Period Template Detail Filter """


class PeriodTemplateDetailFilter(filters.FilterSet):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'




""" PeriodTemplateToGrade Filter """
class PeriodTemplateToGradeFilter(filters.FilterSet):
    section_name = filters.CharFilter(field_name='academic_session__section__name',lookup_expr='icontains')
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'