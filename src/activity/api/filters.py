from activity.models import*
from django_filters import rest_framework as filters


""" Activity filter """


class ActivityFilter(filters.FilterSet):
    class Meta:
        model = Activity
        fields = '__all__'


""" Activity Asset Filter """


class ActivityAssetFilter(filters.FilterSet):
    class Meta:
        model = ActivityAsset
        fields = '__all__'


""" Activity Complete  Filter """


class ActivityCompleteFilter(filters.FilterSet):
    class Meta:
        model = ActivityComplete
        fields = '__all__'
