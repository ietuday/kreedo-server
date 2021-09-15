from functools import partial
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
            print("%%%%%%%%%%%%", ex)
            print("line no", traceback.print_exc())
            logger.debug(ex)
            logger.info(ex)
            return ValidationError(ex)


""" PlanPatchUpdateSerailizer"""


class PlanPatchUpdateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


""" Plan Update Serializer"""


class PlanUpdateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

    def update(self, instance, validated_data):

        try:

            plan_activity = self.context['plan_activity_dict']

            plan_qs = Plan.objects.filter(
                pk=instance.pk).update(**validated_data)
            print("plan_qs----------", plan_qs)
            """ Update Plan Activity"""
            for plan_activity_obj in plan_activity:
                if plan_activity_obj['id']:
                    plan_activity_id = plan_activity_obj.pop('id')

                    plan_activity_qss = PlanActivity.objects.filter(
                        id=plan_activity_id)[0]

                    plan_activity_serializer = PlanActivityCreateSerializer(
                        plan_activity_qss, data=dict(plan_activity_obj), partial=True)
                    if plan_activity_serializer.is_valid():
                        plan_activity_serializer.save()
                        print("UPDATE")
                    else:

                        print("%%%%%5", plan_activity_serializer.errors)
                else:
                    for plan_activity_obj in plan_activity:
                        plan_activity_obj['plan'] = instance.pk

                    """ calling PlanActivityCreate Serializer with order_items data. """

                    plan_activity_serializer = PlanActivityCreateSerializer(
                        data=list(plan_activity), many=True)

                    if plan_activity_serializer.is_valid():
                        plan_activity_serializer.save()
                        print("Plan Activtiy Create")

                    else:
                        print(plan_activity_serializer.errors)

            # plan_activity_qs= PlanActivity.objects.filter
            return instance
        except Exception as ex:
            print("@@@@@@@@ SERIALIZER", ex)
            print("Traceback------>", traceback.print_exc())
            raise ValidationError(ex)


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
            print("serialized_data", serialized_data)
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

                print("attendance_qs", attendance_qs)
                for i, d in enumerate(attendance_qs.childs):

                    if str(child_id) in d['child_id']:

                        print("Child id is present", str(child_id))
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
        depth = 2


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
        depth = 2


class GradeSubjectPlanUpdateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeSubjectPlan
        fields = '__all__'
        depth = 1


class SubjectSchoolGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = ['grade']
        depth = 1


# GradeSubjectPlan


class GradeSubjectPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeSubjectPlan
        fields = ['grade']
        depth = 1


""" SubjectSchoolGradePlan Create Serializer """


class SubjectSchoolGradePlanBySchoolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = '__all__'


class SubjectSchoolGradePlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeSubjectPlan
        fields = '__all__'


""" Grade creation updation deletion Serializer"""


class SubjectSchoolGradePlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeSubjectPlan
        fields = '__all__'

    def create(self, validated_data):
        try:
            print("VALUE------", validated_data)
            print("SELF---->", self.context['grade_label_data'])
            grade_list = self.context['grade_label_data']
            grades_list = []
            for grades in grade_list:
                grades_list.append(grades['grade'])

            for grade in grade_list:
                print("GRADE----------", grade['school'])
                if GradeSubjectPlan.objects.filter(school=grade['school'],
                                                   grade=grade['grade']).exists():
                    print("EXIST")
                    grade_qs = GradeSubjectPlan.objects.filter(school=grade['school'],
                                                               grade=grade['grade'])[0]
                    print("@@@@@@@@@@@@", grade_qs)

                    if SubjectSchoolGradePlan.objects.filter(
                            grade_subjects=grade_qs).exists():
                        print("LABEL update ")
                        grade_label_qs = SubjectSchoolGradePlan.objects.filter(
                            grade_subjects=grade_qs)[0]

                        grade_label_qs.grade_label = grade['grade_label']
                        grade_label_qs.save()
                        print("LABEL SAVE")

                    plan_qs = GradeSubjectPlan.objects.filter(
                        school=grade['school']).exclude(grade__in=grades_list)
                    print("DELETEEE-----------", plan_qs)

                    if plan_qs:
                        plan_qs = plan_qs[0]
                        print("plan_qs id----", plan_qs)
                        plan_id = plan_qs.id

                        grade_delete_qs = SubjectSchoolGradePlan.objects.filter(
                            grade_subjects=plan_id)
                        if grade_delete_qs:
                            grade_delete_qs.delete()

                            plan_qs.delete()
                            print("DELTED")

                else:

                    # grades_list = []
                    print("grade['grade')]--",)
                    school_id = School.objects.filter(id=grade['school'])[0]

                    grade_id = Grade.objects.filter(id=grade['grade'])[0]
                    print("SCHOOL", school_id, grade_id)

                    grade_qs = GradeSubjectPlan.objects.create(
                        grade=grade_id, school=school_id)

                    print("grade_qs", grade_qs.id)

                    grade_subject_plan_dict = {
                        "grade_label": grade['grade_label'],
                        "grade_subjects": [grade_qs.id]
                    }
                    grade_subject_plan_serializer = SubjectSchoolGradePlanBySchoolCreateSerializer(
                        data=dict(grade_subject_plan_dict))
                    if grade_subject_plan_serializer.is_valid():
                        grade_subject_plan_serializer.save()
                        print("CREATE  LABEL")
                    else:
                        print("ERROR-------> in label creation",
                              grade_subject_plan_serializer.errors)

            return validated_data
        except Exception as ex:
            print("ERROR----------", ex)
            print("TRACEBACK-------------", traceback.print_exc())


""" Subject creation , updation , deletion, by school"""


class SubjectSchoolPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectPlan
        fields = '__all__'

    def create(self, validated_data):
        try:
            print("VALUE------", validated_data)
            print("SELF---->", self.context['subject_label_data'])
            subject_list = self.context['subject_label_data']
            subjects_list = []
            for sub in subject_list:
                subjects_list.append(sub['subject'])
            print("subjects_list---->", subjects_list)
            for sub in subject_list:
                print("GRADE----------", sub['school'])
                if SubjectPlan.objects.filter(school=sub['school'], subject=sub['subject']).exists():
                    print("EXIST")
                    subject_qs = SubjectPlan.objects.filter(school=sub['school'],
                                                            subject=sub['subject'])[0]
                    print("@@@@@@@@@@@@", subject_qs)
                    if subject_qs:
                        subject_qs.subject_label = sub['subject_label']
                        subject_qs.save()
                        print(" Subject LABEL update")

                    plan_qs = SubjectPlan.objects.filter(
                        school=sub['school']).exclude(subject__in=subjects_list)
                    print("DELETEEE-----------", plan_qs)

                    if plan_qs:
                        plan_qs = plan_qs[0]
                        print("plan_qs id----", plan_qs)
                        plan_id = plan_qs.id

                        subject_delete_qs = GradeSubjectPlan.objects.filter(
                            subject_plan=plan_id)
                        if subject_delete_qs:
                            print("@@@@@@@", subject_delete_qs)

                            plan_qs.delete()
                            print("DELTED")

                else:
                    # grades_list = []
                    print("sub['subject')]--",)
                    school_id = School.objects.filter(id=sub['school'])[0]

                    subject_id = Subject.objects.filter(id=sub['subject'])[0]
                    print("SCHOOL", school_id, subject_id)

                    subject_qs = SubjectPlan.objects.create(
                        subject=subject_id, school=school_id, subject_label=sub['subject_label'])

                    print("grade_qs", subject_qs.id)
                    grade_qs = GradeSubjectPlan.objects.filter(
                        school=school_id, grade=sub['grade'])[0]
                    grade_qs.subject_plan.add(subject_qs.id)
                    grade_qs.save()
                    print("ADDED in Grade subject plan")

            return validated_data
        except Exception as ex:
            print("ERROR----", ex)
            print("Traceback--------->", traceback.print_exc())


class SubjectSchoolGradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = '__all__'


class GradesBySchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = ['grade', 'school']
        depth = 1
