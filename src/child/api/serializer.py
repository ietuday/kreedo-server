import traceback
from rest_framework import serializers
from child.models import*


""" Child Create Serializer """


class ChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


""" Child List Serializer """


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1


""" Attendance Create Serializer """


class AttendanceCreateSerializer(serializers.ModelSerializer):
    # childs = serializers.JSONField(required=False)
    class Meta:
        model = Attendance
        fields = '__all__'


""" Attendance List Serializer """


class AttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 1
