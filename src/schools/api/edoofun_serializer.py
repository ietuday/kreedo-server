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




class SchoolDetailSerializer(serializers.ModelSerializer):
    account_manager = AccountListForSerializer()
    class Meta:
        model = School
        fields = '__all__'
        depth = 1

   