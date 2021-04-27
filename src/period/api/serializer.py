from rest_framework import serializers
from period.models import*
from rest_framework.validators import UniqueTogetherValidator

""" Period Template Serializer """


class PeriodTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplate
        fields = '__all__'


""" Period List Serializer """


class PeriodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'
        depth = 1


""" Period Create Serializer """

import traceback
class PeriodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['name']
    
    def create(self,validated_data):
        print("Self------------------->", self)
        print("DAtaa", validated_data)
        try:
            print("DAtaa", validated_data)

        except Exception as ex:
            print("Error", ex)
            print("traceback", traceback.print_exc())
    
    


""" Period Template Detail List Serializer """


class PeriodTemplateDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
        depth = 1


""" Period Template Detail Create Serializer """


class PeriodTemplateDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=PeriodTemplateDetail.objects.all(),
                fields=['room', 'start_time','end_time']
            )
        ]
