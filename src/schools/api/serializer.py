from rest_framework import serializers
from ..models import*


""" Grade Serializer """
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

"""Section Serializer """
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

""" Subject Serializer """
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

""" License Serializer"""

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'


""" School  List Serializer"""

class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        depth = 1


""" School create Serializer"""

class SchoolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        
    def create(self, validated_data):
        return School.objects.create(**validated_data)