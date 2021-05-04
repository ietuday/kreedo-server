from rest_framework import serializers
from ..models import*
from django.core.exceptions import ValidationError

""" Plan Type Serializer """


class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanType
        fields = '__all__'


""" Plan List Serilaizer """


class PlanListSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        depth = 1


""" Plan Create Serializer """


class PlanCreateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

    # def to_representation(self, instance):
    #     try:
    #         instance = super(PlanCreateSerailizer,
    #                          self).to_representation(instance)
    #         instance['plan_activity'] = self.context['plan_activity_data']
    #         return instance
    #     except Exception as ex:
    #         print("error")

    def create(self, validated_data):
        try:
            print("@@@", self.context['plan_activity_dict'])
            plan_activity = self.context.pop('plan_activity_dict')
            plan = super(PlanCreateSerailizer, self).create(validated_data)
            print("#############", plan)

            for plan_obj in plan_activity:
                print("%%%%%%%%%%%%", plan_obj)
                plan_obj['plan'] = plan.id

            # """ calling PlanActivityCreate Serializer with order_items data. """

            # plan_activity_serializer = PlanActivityCreateSerializer(
            #     data=list(plan_activity), many=True)

            # if plan_activity_serializer.is_valid(raise_exception=True):
            #     plan_activity_serializer.save()
            #     self.context['plan_activity_data'] = plan_activity_serializer.data
            # else:
            #     print("plan Activity Error", plan_activity_serializer.errors)
            #     raise ValidationError(plan_activity_serializer.errors)

        except Exception as ex:
            print("Error", ex)
            return ValidationError(ex)


""" child Plan List Serailizer"""


class ChildPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = '__all__'
        depth = 1


""" child Plan create Serailizer """


class ChildPlanCreateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = ['child', 'academic_session',
                  'subjects', 'curriculum_start_date']


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
        depth = 1


""" SubjectSchoolGradePlan Create Serializer """


class SubjectSchoolGradePlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchoolGradePlan
        fields = '__all__'
