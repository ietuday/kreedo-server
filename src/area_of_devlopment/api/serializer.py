from rest_framework import serializers
from rest_framework.serializers import (
    SerializerMethodField,
  )
from area_of_devlopment.models import*

""" Area of Devlopment Create Serializer """

class AreaOfDevlopmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfDevlopment
        fields = '__all__'


""" Area of Devlopment List Serializer """

class AreaOfDevlopmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfDevlopment
        fields = '__all__'
        depth = 1


""" Area of Devlopment Update Serializer """

class AreaOfDevlopmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfDevlopment
        fields = '__all__'

""" Conept List Serializer """

""" Skill List Serializer """


class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        depth = 1


class ConceptListSerializer(serializers.ModelSerializer):
    skill = SerializerMethodField()

    class Meta:
        model = Concept
        fields = '__all__'
        depth = 1

    def get_skill(self, obj):
        print("@@@@@@@@", obj)
        try:
            skill_obj = Skill.objects.filter(concept=obj.id)
            print("$$$$$$$$$$$",skill_obj)
            if skill_obj == None:
                return {}
            return SkillListSerializer(skill_obj, many=True).data
        except Exception as e:
            print(e)
            return None


""" Conept Create Serializer """


class ConceptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = '__all__'





""" Skill List Serializer """


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
