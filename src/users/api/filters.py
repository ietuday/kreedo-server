from django_filters.filters import NumberFilter
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
    user_obj = filters.CharFilter(
        field_name='user_obj__username', lookup_expr='icontains')

    class Meta:
        model = UserDetail
        fields = '__all__'


class ReportingToFilter(filters.FilterSet):
    class Meta:
        model = ReportingTo
        fields = '__all__'


class UserRoleFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name='user__user_obj__first_name', lookup_expr='icontains')
    username = filters.CharFilter(
        field_name='user__user_obj__username', lookup_expr='icontains')

    class Meta:
        model = UserRole
        fields = '__all__'


class SchoolUserRoleFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name='user__user_obj__first_name', lookup_expr='icontains')
    username = filters.CharFilter(
        field_name='user__user_obj__username', lookup_expr='icontains')
    pincode = filters.NumberFilter(
        field_name='school__address__pincode')

    class Meta:
        model = UserRole
        fields = '__all__'
