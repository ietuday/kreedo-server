from rest_framework import serializers

from django.contrib.auth.models import User
from ..models import*
from address.api.serializer import AddressSerializer
import traceback

""" Role Model Serializer """
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


""" User Type Serializer """
class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'
        





""" Auth User Serializer """

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['id','username','first_name','last_name','email','is_active']

""" UserDetail Serializer """

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        

""" Reporting To  Serializer """

class ReportingToSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingTo
        fields = '__all__'


""" User Register API """
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id','email','first_name','last_name','password','is_active']
        extra_kwargs = {'password': {'write_only': True}}

    
    def validate(self,validated_data):
        try:
            user_detail_data = self.context['user_detail_data']
            address_detail = self.context['address_detail']
            print("user_detail_data",user_detail_data)
            print("address_detail",address_detail)
            print("validated_data",validated_data)

        except Exception as ex:
            print("error------------", ex)
    
    
    
    # def create(self,validated_data):
    #     print("CREATE@@@@@@@@@@@@@@@@@@", self)
    