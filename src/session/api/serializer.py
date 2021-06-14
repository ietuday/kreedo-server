from holiday.models import*
from users.api.serializer import*
from rest_framework import serializers
from ..models import *
from schools.api.serializer import*
from django.core.exceptions import ValidationError

from holiday.api.serializer import*
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
        # fields = '__all__'
        fields = ['id', 'school', 'grade','academic_calender',
                  'section', 'is_active', 'is_applied']


class AcademicSessionListSerializer(serializers.ModelSerializer):
    class_teacher = UserDetailListForAcademicSessionSerializer()

    class Meta:
        model = AcademicSession
        fields = '__all__'
        depth = 1


""" Grade List of Academic Session """


class GradeListOfAcademicSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcademicSession
        fields = ['grade']
        depth = 1


""" Section List of Academic Session """


class SectionListOfAcademicSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcademicSession
        fields = ['section']
        depth = 2

    # def to_representation(self, obj):
    #     serialized_data = super(
    #         SectionListOfAcademicSessionSerializer, self).to_representation(obj)

    #     section_data = serialized_data.get('section')

    #     grade = section_data.get('grade')
    #     print("GRADE--------------",grade)

    #     return serialized_data


class AcademicCalenderBySchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCalendar
        fields = '__all__'
        # depth = 1


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

    def create(self, validated_data):
        try:
            academic_calender = super(
                AcademicCalenderCreateSerializer, self).create(validated_data)

            holiday_qs = SchoolHoliday.objects.filter(
                school=validated_data['school'], holiday_from__gte=validated_data['start_date'], holiday_till__lte=validated_data['end_date'])

            for holiday in holiday_qs:
                holiday_id = holiday.holiday_type.id
                holiday_by_academic_calender = {
                    "academic_calender": academic_calender.id,
                    "title": holiday.title,
                    "description": holiday.description,
                    "holiday_from": holiday.holiday_from,
                    "holiday_till": holiday.holiday_till,
                    "holiday_type": holiday_id,
                    "is_active": holiday.is_active
                }

                school_holiday_serializer = SchoolHolidayCreateSerializer(
                    data=holiday_by_academic_calender)
                if school_holiday_serializer.is_valid():
                    school_holiday_serializer.save()
                else:

                    raise ValidationError(school_holiday_serializer.errors)

            week_off_by_academic_calender = {
                "academic_calender": academic_calender.id,
                "monday": "false",
                "tuesday": "false",
                "wednesday": "false",
                "thursday": "false",
                "friday": "false",
                "saturday": "false",
                "sunday": "false",
                "is_active": "true"

            }

            week_off_qs_serializer = SchoolWeakOffCreateSerializer(
                data=week_off_by_academic_calender)
            if week_off_qs_serializer.is_valid():
                week_off_qs_serializer.save()
            else:

                raise ValidationError(week_off_qs_serializer.errors)
            return academic_calender

        except Exception as ex:
            print("@#######", ex)
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)


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
