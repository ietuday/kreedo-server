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
        print("serialized_data", serialized_data.get('id'))
        resultant_dict = {}
        grade_qs = SchoolGradeSubject.objects.filter(
        school=serialized_data.get('id')).values('grade')
      
        if grade_qs:
            grade_list = list(
            set(val for dic in grade_qs for val in dic.values()))

            grade_qs = Grade.objects.filter(id__in=grade_list)

            grade_qs_serializer = GradeListSerializer(grade_qs, many=True)

            serialized_data['classes'] = grade_qs_serializer.data
        return serialized_data

   