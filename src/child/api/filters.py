from django_filters import rest_framework as filters
from child.models import*

# """ Child Filter """


class ChildFilter(filters.FilterSet):
    last_name = filters.CharFilter(
        field_name='last_name', lookup_expr='icontains')
    first_name = filters.CharFilter(
        field_name='first_name', lookup_expr='icontains')
    grade = filters.CharFilter(
        field_name='child_plan__academic_session__grade__id')
    section = filters.CharFilter(
        field_name='child_plan__academic_session__section__id')

    class Meta:
        model = Child
        fields = '__all__'


""" Child Detail Filter """


class ChildDetailFilter(filters.FilterSet):
    class Meta:
        model = ChildDetail
        fields = ['child']


""" ChildSession Filter """


class ChildSessionFilter(filters.FilterSet):
    class Meta:
        model = ChildSession
        fields = '__all__'


"""  Attendance filter """


class AttendanceFilter(filters.FilterSet):
    class Meta:
        model = Attendance
        fields = ['academic_session']
