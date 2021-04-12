from rest_framework import serializers
from package.models import *


""" Package List Serializer """


class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        depth = 1


""" Package Create serializer """


class PackageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


""" School Package List Serializer """


class SchoolPackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPackage
        fields = '__all__'
        depth = 1


""" School Package Create Serializer """


class SchoolPackageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPackage
        fields = '__all__'
