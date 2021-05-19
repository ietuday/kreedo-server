from django_filters import rest_framework as filters
from plan.models import*

""" Plan Filter """


class PlanFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    grade = filters.CharFilter(
        field_name='grade__name', lookup_expr='icontains')
    subject = filters.CharFilter(
        field_name='subject__name', lookup_expr='icontains')

    class Meta:
        model = Plan
        fields = '__all__'


""" Child plan Filter """


class ChildPlanFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    child_first_name = filters.CharFilter(
        field_name='child__first_name', lookup_expr='icontains')
    child_last_name = filters.CharFilter(
        field_name='child__last_name', lookup_expr='icontains')
    academic_session_session = child_last_name = filters.CharFilter(
        field_name='academic_session__session__name', lookup_expr='icontains')

    class Meta:
        model = ChildPlan
        fields = '__all__'


"""  Plan Activity Filter"""


class PlanActivityFilter(filters.FilterSet):
    class Meta:
        model = PlanActivity
        fields = '__all__'


""" Subject School Grade  Plan Filter """


class SubjectSchoolGradePlanFilter(filters.FilterSet):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = '__all__'
