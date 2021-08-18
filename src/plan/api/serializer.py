from traceback import print_exc
from child.api.serializer import*
from child.models import*
from session.api.serializer import*
from rest_framework import serializers
from ..models import*
from django.core.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError)
from kreedo.conf.logger import CustomFormatter
import logging
from activity.models import*

""" Logging """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)

""" Plan List Serilaizer """


class PlanListSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        depth = 1

    def to_representation(self, obj):
        serialized_data = super(
            PlanListSerailizer, self).to_representation(obj)

        plan_id = serialized_data.get('id')
        plan_activity = PlanActivity.objects.filter(plan__id=plan_id)
        plan_activity_serializer = PlanActivityListSerializer(
            plan_activity, many=True)
        serialized_data['plan_activity_data'] = plan_activity_serializer.data
        return serialized_data


class PlanSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


""" Plan Create Serializer """


class PlanCreateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

    def to_representation(self, instance):
        try:
            instance = super(PlanCreateSerailizer,
                             self).to_representation(instance)
            instance['plan_activity'] = self.context['plan_activity_serializer_data']
            return instance
        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)

    def create(self, validated_data):
        try:
            print("create called")
            plan_activity = self.context.pop('plan_activity_dict')
            plan = super(PlanCreateSerailizer, self).create(validated_data)

            for plan_activity_obj in plan_activity:
                plan_activity_obj['plan'] = plan.id

            """ calling PlanActivityCreate Serializer with order_items data. """

            plan_activity_serializer = PlanActivityCreateSerializer(
                data=list(plan_activity), many=True)

            if plan_activity_serializer.is_valid():
                plan_activity_serializer.save()
                self.context.update(
                    {"plan_activity_serializer_data": plan_activity_serializer.data})
            else:
                raise ValidationError(plan_activity_serializer.errors)
            return plan
        except Exception as ex:
            print("%%%%%%%%%%%%",ex)
            print("line no",traceback.print_exc())
            logger.debug(ex)
            logger.info(ex)
            return ValidationError(ex)


""" Plan Update Serializer"""
class PlanUpdateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


""" child Plan List Serailizer"""
class ChildPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = '__all__'
        depth = 1

    def to_representation(self, obj):
        serialized_data = super(
            ChildPlanListSerializer, self).to_representation(obj)

        child_data = serialized_data.get('child')
        child_id = child_data.get('id')
        child_activity_count = ActivityComplete.objects.filter(
            child__id=child_id, is_completed=False).count()
        serialized_data['activity_behind'] = child_activity_count
        return serialized_data


class ChildPlanListByGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = ['child']
        depth = 1

    def to_representation(self, obj):
        try:
            serialized_data = super(
                ChildPlanListByGradeSerializer, self).to_representation(obj)
            print("serialized_data",serialized_data)
            child_data = serialized_data.get('child')
            child_id = child_data.get('id')
            child_activity_count = ActivityComplete.objects.filter(
                child__id=child_id, is_completed=False).count()
            # pdb.set_trace()
            serialized_data['activity_behind'] = child_activity_count
            if Attendance.objects.filter(attendance_date=self.context['attendance_detail']['attendance_date'],
                                         academic_session=self.context['attendance_detail']['academic_session']).exists():
                attendance_qs = Attendance.objects.get(attendance_date=self.context['attendance_detail']['attendance_date'],
                                                       academic_session=self.context['attendance_detail']['academic_session'])

                print("attendance_qs",attendance_qs)
                for i, d in enumerate(attendance_qs.childs):
                    
                    if str(child_id) in d['child_id']:
                        
                        print("Child id is present",str(child_id) )
                        serialized_data['is_present'] = d['present']
                        # return serialized_data
                    else:
                        serialized_data['is_present'] = False
                        # return serialized_data

            else:
                serialized_data['is_present'] = False
            return serialized_data
        except Exception as ex:
            print("ex", ex)
            print(traceback.print_exc())


""" child plan activity Serializer """


class ChildPlanActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = '__all__'
        depth = 3


class ChildPlanForChildSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = '__all__'


""" child Plan create Serailizer """


class ChildPlanCreateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = ['child', 'academic_session',
                  'subjects', 'curriculum_start_date']


class ChildPlanUpdateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = '__all__'


class ChildPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = ['academic_session']
        depth = 2


class ChildPlanOfChildSerializer(serializers.ModelSerializer):
    academic_session = AcademicSessionListForChildSerializer()

    class Meta:
        model = ChildPlan
        fields = '__all__'
        # depth = 1


class ChildPlansChildSerializer(serializers.ModelSerializer):
    # child = SerializerMethodField()
    class Meta:
        model = ChildPlan
        fields = ['id', 'child', 'is_active']
        depth = 1

    # def to_representation(self, obj):
    #     print("#############", obj)
        # serialized_data = super(
        #     ChildPlanListSerializer, self).to_representation(obj)

        # child_data = serialized_data.get('child')
        # child_id = child_data.get('id')
        # child_activity_count = ActivityComplete.objects.filter(
        #     child__id=child_id, is_completed=False).count()
        # serialized_data['activity_behind'] = child_activity_count
        # return serialized_data


""" Plan activity List Serializer """


class PlanActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanActivity
        fields = '__all__'


""" Plan Activity Create Serilaizer """


class PlanActivityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanActivity
        fields = '__all__'


""" SubjectSchoolGradePlan List Serializer """


class SubjectSchoolGradePlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = '__all__'
        depth = 1


""" SubjectSchoolGradePlan Create Serializer """


class SubjectSchoolGradePlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = '__all__'
