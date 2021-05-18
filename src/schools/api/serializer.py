from rest_framework import serializers
from ..models import*


""" Grade Serializer """


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


"""Section List Serializer """


class SectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        depth = 1


"""Section Create Serializer """


class SectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


""" Subject List Serializer """


class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        depth = 1


""" Subject Create Serializer """


class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


""" License List Serializer"""


class LicenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'
        depth = 1


""" License Create Serializer"""


class LicenseCreateSerializer(serializers.ModelSerializer):
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


""" Section Subject Teacher List Serializer """


class SectionSubjectTeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionSubjectTeacher
        fields = '__all__'
        depth = 1


""" Section Subject Teacher Create Serializer """


class SectionSubjectTeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionSubjectTeacher
        fields = '__all__'


""" Room List Serializer """


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        depth = 1


""" Room create Serializer """


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class SchoolGradeSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGradeSubject
        fields = '__all__'
