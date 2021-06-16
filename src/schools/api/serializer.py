from rest_framework import serializers
from ..models import*


""" Grade Serializer """


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def to_representation(self, obj):
        serialized_data = super(
            GradeListSerializer, self).to_representation(obj)


      
        grade_id = serialized_data.get('id')

        section_qs = Section.objects.filter(grade__in=str(grade_id))
        section_qs_serializer = SectionSerializer(section_qs, many=True)
        serialized_data['sections']= section_qs_serializer.data

        return serialized_data





"""Section List Serializer """


class SectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        depth = 1



class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        



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



""" School  List Serializer"""

from users.models import*
from users.api.serializer import*
class SchoolDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        depth = 1

    
    def to_representation(self, obj):
        serialized_data = super(
            SchoolDetailListSerializer, self).to_representation(obj)

        school_data_id = serialized_data.get('id')
        print("School",school_data_id)
        
        user_role_qs = UserRole.objects.filter(
            school=school_data_id).values('user').distinct()
        print("user_role_qs-",user_role_qs)
        user_detail_qs = UserDetail.objects.filter(user_obj__in=user_role_qs)
        print("USER- DETAIL", user_detail_qs)
        user_detail_qs_serializer = UserDetailListSerializer(user_detail_qs, many=True)


        serialized_data['user_list'] = user_detail_qs_serializer.data
        return serialized_data



""" School create Serializer"""


class SchoolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

    def create(self, validated_data):
        return School.objects.create(**validated_data)


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

    def create(self, validated_data):
        try:
            school_package = self.context.pop('school_package_dict')
            plan = super(SchoolSerializer, self).create(validated_data)

            for school_package_obj in school_package:
                school_package_obj['plan'] = plan.id

            """ calling SchoolPackageCreateSerializer  with school_package data. """

            school_package_serializer = SchoolPackageCreateSerializer(
                data=list(school_package), many=True)

            if school_package_serializer.is_valid():
                school_package_serializer.save()
                self.context.update(
                    {"school_package_serializer_data": school_package_serializer.data})
            else:
                raise ValidationError(school_package_serializer.errors)
            return plan
        except Exception as ex:
            logger.debug(ex)
            logger.info(ex)
            return ValidationError(ex)


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

class RoomBySchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
    # def to_representation(self, obj):
    #     serialized_data = super(
    #         RoomListSerializer, self).to_representation(obj)

    #     school_id = serialized_data.get('school')
    #     school_id = subject_qs.get('id')
    #     subject_qs = SchoolGradeSubject.objects.filter(
    #         school=school_id)
    #     subject_serializer = SchoolGradeSubjectSerializer(subject_qs,many=True)
    #     serialized_data['subject'] = subject_serializer.data
    #     return serialized_data

""" Room create Serializer """


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


# class SchoolGradeSubjeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SchoolGradeSubject
#         fields = '__all__'


""" SchoolGradeSubject List Serializer """


class SchoolGradeSubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGradeSubject
        fields = '__all__'
        depth = 1


""" SchoolGradeSubject Create Serializer """


class SchoolGradeSubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGradeSubject
        fields = '__all__'


""" SchoolGradeSubject  Serializer """


class SchoolGradeSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGradeSubject
        fields = ['grade']
        depth = 1


""" SchoolGradeSubject List Serializer """


class SubjectBySchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGradeSubject
        fields = ['subject']
        depth = 1
