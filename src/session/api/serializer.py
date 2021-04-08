from rest_framework import serializers
from ..models import *



class SchoolSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSession
        fields = '__all__'