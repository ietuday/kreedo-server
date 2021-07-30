import traceback
from rest_framework import serializers
from .utils import*
import logging
from ..models import*




""" Skill List Serializer """


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        depth=1


class SkillConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['concept']
        depth=1



class SkillListForChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        
