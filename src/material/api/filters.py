from django_filters import rest_framework as filters
from material.models import*


"""Material Filter """


class MaterialFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    decription = filters.CharFilter(
        field_name='decription', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = Material
        fields = '__all__'


""" ActivityMasterSupportingMaterial Filter """


class ActivityMasterSupportingMaterialFilter(filters.Filter):
    class Meta:
        model = ActivityMasterSupportingMaterial
        fields = '__all__'
