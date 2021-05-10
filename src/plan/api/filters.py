from django_filters import rest_framework as filters
from plan.models import*

""" Plan Filter """


class PlanFilter(filters.FilterSet):
    class Meta:
        model = Plan
        fields = '__all__'


""" Child plan Filter """


class ChildPlanFilter(filters.FilterSet):
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
