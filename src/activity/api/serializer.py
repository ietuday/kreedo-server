from rest_framework import serializers
from activity.models import*


""" Activity List Serializer """


class ActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        depth = 1


""" Activity Create Serializer """


class ActivityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


""" Activity Asset List Serializer"""


class ActivityAssetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAsset
        fields = '__all__'
        depth = 2


""" Activity Asset Create Serializer"""


class ActivityAssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAsset
        fields = '__all__'


""" Group Activity Missed List Serializer"""


class GroupActivityMissedListSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = GroupActivityMissed
        fields = '__all__'
        depth = 1


""" Group Activity Missed Create Serializer"""


class GroupActivityMissedCreateSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = GroupActivityMissed
        fields = '__all__'
