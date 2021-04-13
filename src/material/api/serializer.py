from rest_framework import serializers
from material.models import*

""" Matetril Serializer """


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


""" ActivityMasterSupportingMaterial List Serailizer """


class ActivityMasterSupportingMaterialListSerializer(serializers.ModelSerializer):
    model = ActivityMasterSupportingMaterial
    fields = '__all__'
    depth = 1


""" ActivityMasterSupportingMaterial Create Serailizer """


class ActivityMasterSupportingMaterialCreateSerializer(serializers.ModelSerializer):
    model = ActivityMasterSupportingMaterial
    fields = '__all__'
