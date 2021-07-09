from rest_framework import serializers
from ..models import*


class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        depth = 1
