from django.contrib.auth.models import User
from users.api.edoofun_serializer import *
from rest_framework import serializers
from ..models import *
from django.core.exceptions import ValidationError
from kreedo.conf.logger import CustomFormatter
import logging
from users.models import*
# from users.api.edoofun_serializer import*

""" Logging """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)


class AuthUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_active']


class AccountsUserSerializer(serializers.ModelSerializer):

    user_obj = AuthUsersSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 3

    """ no of license add """

    def to_representation(self, obj):
        serialized_data = super(
            AccountsUserSerializer, self).to_representation(obj)
        user_id = serialized_data['user_obj']['id']
        role_id = [entry['id'] for entry in serialized_data['role']]

        user_role = UserRole.objects.filter(
            user=user_id, role=role_id[0], school__isnull=False).count()
        if user_role:
            serialized_data['no_of_license'] = user_role

        return serialized_data


""" Section List Serializer """


class SectionListBySchoolSerializer(serializers.ModelSerializer):
    class_teacher = AccountsUserSerializer()

    class Meta:
        model = AcademicSession
        fields = ['section', 'grade', 'class_teacher']
        depth = 1


class LicenceUserSerializer(serializers.ModelSerializer):

    user_obj = AuthUsersSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 3


class AcademicSessionGradeSerializer(serializers.ModelSerializer):
    class_teacher = LicenceUserSerializer()

    class Meta:
        model = AcademicSession
        fields = '__all__'
        depth = 1


class ClassTeacherSerializer(serializers.ModelSerializer):

    user_obj = AuthUsersSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires',
                   'address', 'type', 'role', 'reason_for_discontinution', 'relationship_with_child', 'joining_date', 'secret_pin')
        depth = 3


class AcademicSessionChildSerializer(serializers.ModelSerializer):
    class_teacher = ClassTeacherSerializer()

    class Meta:
        model = AcademicSession
        fields = ['school', 'grade', 'section', 'class_teacher']
        depth = 1
