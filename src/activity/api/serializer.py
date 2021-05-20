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

class ActivityAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAsset
        fields = '__all__'

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


class ActivityCompleteSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = ActivityComplete
        fields = ['activity', 'period']
        depth = 2

    def to_representation(self, obj):
        serialized_data = super(
            ActivityCompleteSerilaizer, self).to_representation(obj)
        activity_data = serialized_data.get('activity')
        
        activity_id = activity_data.get('id')
        activity_asset_qs = ActivityAsset.objects.filter(activity__id=activity_id)
        activity_asset_serializer = ActivityAssetSerializer(
            activity_asset_qs, many=True)
        serialized_data['activity_asset_data'] = activity_asset_serializer.data
        return serialized_data



""" Activity  Complete Create Serializer"""


class ActivityCompleteCreateSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ActivityComplete
        fields = '__all__'
