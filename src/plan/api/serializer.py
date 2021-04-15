from rest_framework import serializers
from ..models import*


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
        fields = '__all__'


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
