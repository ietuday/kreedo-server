from rest_framework import serializers
from ..models import*
from users.api.edoofun_serializer import*




class LicenseSerializer(serializers.ModelSerializer):
    created_by = AccountListForSerializer()
    class Meta:
        model = License
        fields = '__all__'
        depth = 2


class SchoolListSerializer(serializers.ModelSerializer):
    license=  LicenseSerializer()
    # account_manager = AccountListForSerializer()
    class Meta:
        model = School
        fields = '__all__'
        depth = 1



from .serializer import*
from session.api.edoofun_serializer import*
class SchoolDetailSerializer(serializers.ModelSerializer):
    account_manager = AccountListForSerializer()
    license=  LicenseSerializer()
    class Meta:
        model = School
        fields = '__all__'
        depth = 1

    def to_representation(self, obj):
        serialized_data = super(
            SchoolDetailSerializer, self).to_representation(obj)
        resultant_dict = {}
        grade_qs = AcademicSession.objects.filter(
        school=serialized_data.get('id'))
        
        
        if grade_qs:
            

            grade_qs_serializer = SectionListBySchoolSerializer(grade_qs, many=True)

            serialized_data['classes'] = grade_qs_serializer.data
        return serialized_data



class GradeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
        

    def to_representation(self, obj):
        serialized_data = super(
            GradeDetailSerializer, self).to_representation(obj)

        grade_id = serialized_data.get('id')
        section_qs = Section.objects.filter(grade=grade_id)
        section_qs_serializer = SectionDetailSerializer(section_qs, many=True)
        serialized_data['sections'] = section_qs_serializer.data

        return  serialized_data['sections'] 



class SectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        depth = 1