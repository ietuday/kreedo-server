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
