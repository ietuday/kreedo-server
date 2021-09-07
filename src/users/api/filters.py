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
    first_name = filters.CharFilter(
        field_name='user_obj__first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(
        field_name='user_obj__last_name', lookup_expr='icontains')
    email = filters.CharFilter(
        field_name='user_obj__email', lookup_expr='icontains')
    country = filters.CharFilter(
        field_name='address__country', lookup_expr='icontains')
    state = filters.CharFilter(
        field_name='address__state', lookup_expr='icontains')
    city = filters.CharFilter(
        field_name='address__city', lookup_expr='icontains')
    pincode = filters.NumberFilter(
        field_name='address__pincode', lookup_expr='icontains')
    phone = filters.NumberFilter(
        field_name='phone', lookup_expr='icontains')
    address = filters.CharFilter(
        field_name='address__address', lookup_expr='icontains')
    # date = filters.DateFilter(field_name='joining_date__date')

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
    country = filters.CharFilter(
        field_name='user__address__country', lookup_expr='icontains')
    state = filters.CharFilter(
        field_name='user__address__state', lookup_expr='icontains')
    city = filters.CharFilter(
        field_name='user__address__city', lookup_expr='icontains')
    pincode = filters.NumberFilter(
        field_name='user__address__pincode', lookup_expr='icontains')
    phone = filters.NumberFilter(
        field_name='phone', lookup_expr='icontains')
    address = filters.CharFilter(
        field_name='address__address', lookup_expr='icontains')
    school = filters.CharFilter(
        field_name='school__name', lookup_expr='icontains')

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
