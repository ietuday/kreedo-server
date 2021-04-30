from rest_framework import serializers
from ..models import *


class SchoolSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSession
        fields = '__all__'


class AcademicSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'


class AcademicSessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'
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
