from ..models import*
from django_filters import rest_framework as filters


class RoleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Role
        fields = '__all__'


class UserTypeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = UserType
        fields = '__all__'


class UserDetailFilter(filters.FilterSet):

    class Meta:
        model = UserDetail
        fields = '__all__'


class ReportingToFilter(filters.FilterSet):
    class Meta:
        model = ReportingTo
        fields = '__all__'
