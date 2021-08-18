from rest_framework import serializers
from ..models import *
from django.core.exceptions import ValidationError
from kreedo.conf.logger import CustomFormatter
from users.api.edoofun_serializer import *
import logging

from session.api.edoofun_serializer import*
""" Logging """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())


class ChildPlanSectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = ['child']
        depth = 1


class ChildPlanByChildSerializer(serializers.ModelSerializer):
    academic_session = AcademicSessionChildSerializer()

    class Meta:
        model = ChildPlan
        fields = ['child', 'academic_session']
        # depth = 1
