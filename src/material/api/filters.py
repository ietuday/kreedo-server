from django_filters import rest_framework as filters
from material.models import*


"""Material Filter """


class MaterialFilter(filters.FilterSet):
    class Meta:
        model = Material
        fields = '__all__'


""" ActivityMasterSupportingMaterial Filter """


class ActivityMasterSupportingMaterialFilter(filters.Filter):
    class Meta:
        model = ActivityMasterSupportingMaterial
        fields = '__all__'
