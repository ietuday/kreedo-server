from ..models import*
from django_filters import rest_framework as filters
from django_filters import DateRangeFilter,DateFilter

class SchoolTypeFilter(filters.FilterSet):
    class Meta:
        model = SchoolType
        fields = '__all__'

class SchoolLicenseFilter(filters.FilterSet):
    license_from_range = DateRangeFilter(field_name='license_from')
    license_till_range = DateRangeFilter(field_name='license_till')

    class Meta:
        model = SchoolLicense
        fields = '__all__'

class SchoolFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = School
        fields = '__all__'