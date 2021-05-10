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


""" Activity  Complete List Serializer"""


class ActivityCompleteListSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ActivityComplete
        fields = '__all__'
        depth = 3


""" Activity  Complete Create Serializer"""


class ActivityCompleteCreateSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ActivityComplete
        fields = '__all__'
