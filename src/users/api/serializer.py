from rest_framework import serializers
from ..models import*
from django.contrib.auth.models import User


""" Role Model Serializer """
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

""" Auth User Serializer """

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id','username','first_name','last_name','email','is_active']

""" UserDetail Serializer """

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        

""" Reporting To  Serializer """

class ReportingToSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingTo
        fileds = '__all__'