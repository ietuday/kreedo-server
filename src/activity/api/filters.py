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


""" Group Activity Missed Filter """


class GroupActivityMissedFilter(filters.FilterSet):
    class Meta:
        model = GroupActivityMissed
        fields = '__all__'
