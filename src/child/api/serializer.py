from rest_framework import serializers
from child.models import*


""" Child Create Serializer """


class ChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


""" Child List Serializer """


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1
