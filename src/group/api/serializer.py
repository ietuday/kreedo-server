from django.contrib.auth.models import Group,Permission
from rest_framework import serializers

""" Group List and Create Serializer """
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'




""" Permisssion List and Create Serializer """
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'