from rest_framework import serializers
from ..models import*
from users.api.edoofun_serializer import*

from .serializer import*
from session.api.edoofun_serializer import*


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
<<<<<<< HEAD
            SchoolDetailSerializer, self).to_representation(obj)
        resultant_dict = {}
        grade_qs = AcademicSession.objects.filter(
        school=serialized_data.get('id'))
        
        
        if grade_qs:
            

=======
        SchoolDetailSerializer, self).to_representation(obj)
        resultant_dict = {}
        grade_qs = AcademicSession.objects.filter(
        school=serialized_data.get('id'))

        print("###############",grade_qs)
        if grade_qs:
>>>>>>> 1e018a60399e1282bfde29b49b697686490e8727
            grade_qs_serializer = SectionListBySchoolSerializer(grade_qs, many=True)

            serialized_data['classes'] = grade_qs_serializer.data
        return serialized_data



