from rest_framework import serializers
from area_of_devlopment.models import*

""" Area of Devlopment Serializer """


class AreaOfDevlopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfDevlopment
        fields = '__all__'


""" Conept Serializer """


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = '__all__'


""" Skill List Serializer """


class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        depth = 1


""" Skill List Serializer """


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
