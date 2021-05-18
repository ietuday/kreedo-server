from django_filters import rest_framework as filters
from child.models import*

# """ Child Filter """


class ChildFilter(filters.FilterSet):
    last_name = filters.CharFilter(
        field_name='last_name', lookup_expr='icontains')
    first_name = filters.CharFilter(
        field_name='first_name', lookup_expr='icontains')

    class Meta:
        model = Child
        fields = '__all__'


""" Child Detail Filter """


class ChildDetailFilter(filters.FilterSet):
    class Meta:
        model = ChildDetail
        fields = ['child']


"""  Attendance filter """


class AttendanceFilter(filters.FilterSet):
    class Meta:
        model = Attendance
        fields = ['academic_session']
