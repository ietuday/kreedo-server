from ..models import*
from django_filters import rest_framework as filters

class RoleFilter(filters.FilterSet):
    class Meta:
        model = Role
        fields = '__all__'
    
class UserTypeFilter(filters.FilterSet):
    class Meta:
        model = UserType
        fields = '__all__'

class UserDetailFilter(filters.FilterSet):
    school_name = filters.CharFilter(field_name='school__name',lookup_expr='icontains')
    class Meta:
        model = UserDetail
        fields = ['user_obj','phone','address',
                'email_verified','phone_verified','school_name']


class ReportingToFilter(filters.FilterSet):
    class Meta:
        model = ReportingTo
        fields = '__all__'

