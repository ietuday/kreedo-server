import traceback
from rest_framework import serializers
import material
from material.models import Material
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


class SchoolPackageByAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPackage
        fields = ['id', 'package', 'custom_materials']
        depth = 1


class PackageMaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['materials']
        depth = 1


""" School Package Create Serializer """


class SchoolPackageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPackage
        fields = '__all__'


class SchoolPackageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPackage
        fields = '__all__'

    def update(self, instance, validated_data):

        try:

            print("validated_data", validated_data)
            print("instance----------", instance)
            school_package_qs = SchoolPackage.objects.filter(
                pk=instance.pk)[0]
            print("Update", school_package_qs)
            school_package_qs.school = validated_data.get('school', None)
            school_package_qs.package = validated_data.get('package', None)
            material_list = validated_data.get('custom_materials', None)
            materials = []
            for material in material_list:

                material_qs = Material.objects.filter(name=material)[0]
                material_id = material_qs.id
                materials.append(material_id)
            print("$###########3", materials)
            school_package_qs.custom_materials.set(materials)

            school_package_qs.save()
            print("Update package")
            return validated_data

        except Exception as ex:
            print("@@@@@@@@ SERIALIZER", ex)
            print("Traceback------>", traceback.print_exc())
            # raise ValidationError(ex)
