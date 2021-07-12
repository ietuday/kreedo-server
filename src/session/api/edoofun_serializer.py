from rest_framework import serializers
from ..models import *
from django.core.exceptions import ValidationError
from kreedo.conf.logger import CustomFormatter
from users.api.edoofun_serializer import *
import logging


""" Logging """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)

""" Section List Serializer """


class SectionListBySchoolSerializer(serializers.ModelSerializer):
    class_teacher = AccountUserSerializer()
    class Meta:
        model = AcademicSession
        fields = ['section','grade','class_teacher']
        depth = 1





