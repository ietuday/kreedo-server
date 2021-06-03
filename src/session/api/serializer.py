from users.api.serializer import*
from rest_framework import serializers
from ..models import *
from schools.api.serializer import*
from django.core.exceptions import ValidationError


from kreedo.conf.logger import CustomFormatter
import logging


""" Logging """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)

""" School  Session List Serializer """


class SchoolSessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSession
        fields = '__all__'


""" School  Session Create Serializer """


class SchoolSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSession
        fields = '__all__'


""" Academic Session serializer """


class AcademicSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'


class AcademicSessionListSerializer(serializers.ModelSerializer):
    class_teacher = UserDetailListForAcademicSessionSerializer()

    class Meta:
        model = AcademicSession
        fields = '__all__'
        depth = 1


class AcademicSessionListForChildSerializer(serializers.ModelSerializer):
    class_teacher = UserDetailListForAcademicSessionSerializer()

    class Meta:
        model = AcademicSession
        fields = '__all__'
        depth = 1


class AcademicSessionTeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['class_teacher']
        depth = 1


""" AcademicCalender List Seriliazer """


class AcademicCalenderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalender
        fields = '__all__'
        depth = 1


""" AcademicCalender Create Serializer """


class AcademicCalenderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalender
        fields = '__all__'


""" SchoolCalendar List Seriliazer """


class SchoolCalendarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCalendar
        fields = '__all__'
        depth = 1


""" SchoolCalendar Create Serializer """


class SchoolCalendarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCalendar
        fields = '__all__'
