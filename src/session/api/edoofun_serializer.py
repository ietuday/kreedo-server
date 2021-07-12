from rest_framework import serializers
from ..models import *
from django.core.exceptions import ValidationError
from kreedo.conf.logger import CustomFormatter
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
    class Meta:
        model = AcademicSession
        fields = ['section']
        depth = 1
