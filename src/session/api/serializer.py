
from holiday.models import*
from users.api.serializer import*
from rest_framework import serializers
from ..models import *
from schools.api.serializer import *
from django.core.exceptions import ValidationError
from django.db.models import Q, fields
from holiday.api.serializer import *
from kreedo.conf.logger import CustomFormatter
import logging
import traceback
from django.contrib.auth.models import User


""" Logging """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)


class GradeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


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


class teacherAuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_active']


class TeacherListForAcademicSessionSerializer(serializers.ModelSerializer):
    user_obj = teacherAuthUserSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        # depth = 1


""" Academic Session serializer """


class AcademicSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        # fields = '__all__'
        fields = ['id', 'school', 'grade', 'academic_calender', 'session_from', 'session_till',
                  'section', 'is_active', 'is_applied']

    def validate(self, validated_data):
        session_from = validated_data['session_from']
        session_till = validated_data['session_till']
        record_aval = AcademicSession.objects.filter(
            # academic_calender=validated_data['academic_calender'],
            school=validated_data['school'],
            grade=validated_data['grade'],
            section=validated_data['section']
        ).exclude(
            Q(session_till__lt=session_from) |
            Q(session_from__gt=session_till)
        )

        print("record_aval@@", record_aval)
        # pdb.set_trace()
        if record_aval:
            raise ValidationError("Academic Session Over-Lap")
        else:

            return validated_data


class AcademicSessionListSerializer(serializers.ModelSerializer):
    class_teacher = TeacherListForAcademicSessionSerializer()

    class Meta:
        model = AcademicSession
        fields = '__all__'
        depth = 1

    def to_representation(self, obj):
        from schools.api.serializer import AcademicSessionSectionSubjectTeacherListSerializer
        serialized_data = super(
            AcademicSessionListSerializer, self).to_representation(obj)

        academic_session_id = serialized_data.get('id')
        academic_session_qs = SectionSubjectTeacher.objects.filter(
            academic_session=academic_session_id)
        academic_session_qs_serializer = AcademicSessionSectionSubjectTeacherRetriveSerializer(
            academic_session_qs, many=True)
        serialized_data['subject_teacher_list'] = academic_session_qs_serializer.data
        return serialized_data


class AssociateSeactionListSerializer(serializers.ModelSerializer):
    class_teacher = TeacherListForAcademicSessionSerializer()

    class Meta:
        model = AcademicSession
        fields = ['academic_calender', 'grade', 'section',
                  'class_teacher', 'id', 'updated_at', 'created_at', 'is_active']
        depth = 1

    def to_representation(self, obj):
        try:
            from schools.api.serializer import AcademicSessionSectionSubjectTeacherListSerializer
            serialized_data = super(
                AssociateSeactionListSerializer, self).to_representation(obj)

            academic_session_id = serialized_data.get('id')
            academic_session_qs = SectionSubjectTeacher.objects.filter(
                academic_session=academic_session_id)
            academic_session_qs_serializer = AcademicSessionSectionSubjectTeacherRetriveSerializer(
                academic_session_qs, many=True)
            serialized_data['subject_teacher_list'] = academic_session_qs_serializer.data
            return serialized_data
        except Exception as ex:
            print("ERROR--->", ex)
            print(traceback.print_exc())


class AcademicSessionRetriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'
        depth = 1


class AcademicSessionForGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['grade']
        # depth = 1

    def to_representation(self, obj):
        serialized_data = super(
            AcademicSessionForGradeSerializer, self).to_representation(obj)
        # grade_dict = {}
        if obj.grade:
            grade_serializer = GradeSessionSerializer(obj.grade)
            data = grade_serializer.data
            # grade_dict.update(data)

        else:
            data = {}
        return data


class AcademicSessionForCalender(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'


""" Grade List of Academic Session """


class GradeListOfAcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['grade']
        depth = 1


""" Class Teacher by academic session """


class ClassTeacherByAcademicSession(serializers.ModelSerializer):
    class_teacher = TeacherListForAcademicSessionSerializer()

    class Meta:
        model = AcademicSession
        fields = ['id', 'class_teacher', 'academic_calender', 'is_active']
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
        model = AcademicCalender
        fields = '__all__'
        # depth = 1


class AcademicSessionListForChildSerializer(serializers.ModelSerializer):
    class_teacher = TeacherListForAcademicSessionSerializer()

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

    def validate(self, validated_data):
        try:
            print("validate called")
            start_date = validated_data['start_date']
            end_date = validated_data['end_date']
            # academic_cal_aval = AcademicCalender.objects.filter(
            #                             school = validated_data['school'],
            # ).exclude(
            #     Q(end_date__lte=start_date) |
            #     Q(start_date__gte=end_date)
            # )
            academic_cal_aval = AcademicCalender.objects.filter(
                school=validated_data['school'],
                start_date=start_date,
                end_date=end_date
            )

            print("acdemic cal aval", academic_cal_aval)
            # pdb.set_trace()
            # academic_cal_aval = []
            if academic_cal_aval:
                raise ValidationError(
                    "Academic calender with this date already exists")
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


class SchoolCalendarSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCalendar
        fields = '__all__'
        depth = 1


""" SchoolCalendar Create Serializer """


class SchoolCalendarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCalendar
        fields = '__all__'


class AcademicSessionGroupBySection(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['section']
        depth = 1


class AcademicSessionSectionSubjectTeacherRetriveSerializer(serializers.ModelSerializer):
    teacher = UserDetailListForSectionSubjectSerializer()

    class Meta:
        model = SectionSubjectTeacher
        fields = ['subject', 'teacher', 'id']
        depth = 1


class AcademicSessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ['section', 'grade', 'class_teacher',
                  'school', 'academic_calender']


""" Logged In User Serializer """


class LoggedInUserMobSerializer(serializers.ModelSerializer):

    user_obj = AuthUserSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 2

    def to_representation(self, obj):
        from session.api.serializer import AcademicSessionListSerializer
        serialized_data = super(
            LoggedInUserMobSerializer, self).to_representation(obj)

        user_obj_id = serialized_data.get('user_obj')

        user_id = user_obj_id.get('id')
        if UserRole.objects.filter(user=user_id).exists():
            user_role_data = UserRole.objects.filter(user=user_id)
            user_role_data_serializer = UserRoleListSerializer(
                user_role_data, many=True)
            serialized_data['user_role_data'] = user_role_data_serializer.data
        if AcademicSession.objects.filter(class_teacher=user_id).exists():
            # acadamic_session_serializer = AcademicSessionListSerializer(
            #     AcademicSession.objects.filter(class_teacher=user_id), many=True)

            serialized_data['is_ClassTeacher'] = True
        else:
            serialized_data['is_ClassTeacher'] = False

        subject_teacher_list = SectionSubjectTeacher.objects.filter(
            teacher=obj
        )
        if subject_teacher_list:
            # section_subject_serializer = SectionSubjectTeacherCreateSerializer(subject_teacher_list,many=True)
            serialized_data['is_SubjectTeacher'] = True
        else:
            serialized_data['is_SubjectTeacher'] = False
        return serialized_data
