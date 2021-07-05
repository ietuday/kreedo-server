import logging
import traceback
from .edoofun_utils import*
from address.api.serializer import AddressSerializer
from ..models import*
from kreedo.general_views import Mixins, GeneralClass

from rest_framework import serializers
"""
    Django Files
"""
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError)
from django.core.exceptions import ValidationError


from kreedo.conf import logger
from kreedo.conf.logger import CustomFormatter
import logging

""" Logger Function """


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")


""" UserDetail Serializer """


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')


""" User Role Serializer"""


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

    def create(self, validated_data):

        print("User Role Called--------->", validated_data)
        return UserRole.objects.create(**validated_data)


""" Register Parent Serializer """


class RegisterParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def to_representation(self, instance):
        try:
            instance = super(RegisterParentSerializer,
                             self).to_representation(instance)
            """ Update details in RESPONSE """
            print("self.context['user_detail']", self.context)
            instance['user_detail_data'] = self.context['user_detail']

            return instance
        except Exception as ex:
            raise ValidationError(ex)

    def create(self, validated_data):

        try:
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            email = validated_data['email']
            auth_user_created = False
            user_role_created = False

            """ Validate Email """
            try:
                if not email:
                    raise ValidationError("Email is required")
                else:
                    email = user_validate_email(email)
                    if email is True:
                        validated_data['email'] = validated_data['email'].lower(
                        ).strip()
                    else:
                        raise ValidationError(
                            "Enter a valid email address")
            except ValidationError:
                raise ValidationError(
                    "Enter a valid email address")

            """ Genrate Username """
            try:
                username = create_username()
                validated_data['username'] = username

            except ValidationError:
                raise ValidationError("Failed to genrate username")

            """ Genrate Password """
            try:
                genrated_password = create_password(8)
            except Exception as ex:
                raise ValidationError("Failed to Genrate Password")

            try:
                if User.objects.filter(email=validated_data['email']).exists():
                    # raise ValidationError("Email is already Exists")
                    user_obj_id = User.objects.filter(
                        email=validated_data['email'])[0].id

                    phone_no = self.context['user_detail_data']['phone']

                    if UserDetail.objects.filter(user_obj=user_obj_id, phone=phone_no).exists():
                        raise ValidationError("provide corrrect regsitered no")
                elif UserDetail.objects.filter(phone=self.context['user_detail_data']['phone']).exists():
                    raise ValidationError(
                        "Phone already regsitered for another user provide different number.")

                else:

                    """ Create User """
                    user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], first_name=first_name,
                                                    last_name=last_name, is_active=True)
                    user.set_password(genrated_password)
                    user.save()
                    auth_user_created = True

                    self.context['user_detail_data']['user_obj'] = user.id

                    """ Pass request data of User detail Serializer"""

                    user_detail_serializer = UserDetailsSerializer(
                        data=self.context['user_detail_data'])
                    if user_detail_serializer.is_valid():
                        user_detail_serializer.save()

                        self.context.update(
                            {"user_detail": user_detail_serializer.data})

                    else:
                        raise ValidationError(user_detail_serializer.errors)

                    user_role = {
                        "user": user_detail_serializer.data['user_obj'],
                        "role": Role.objects.filter(name="Primary")[0].id,
                        "school": ""
                    }
                    user_role_serializer = UserRoleSerializer(
                        data=dict(user_role))
                    if user_role_serializer.is_valid():
                        user_role_serializer.save()
                        self.context.update({
                            "user_role": user_role_serializer.data
                        })
                    else:
                        raise ValidationError(user_role_serializer.errors)
                    return user

            except Exception as ex:
                print("ERROR-----", ex)
                print("TRACEBACK", traceback.print_exc())
                raise ValidationError(ex)

        except Exception as ex:
            print("errror", ex)
            print("TRACEBACK", traceback.print_exc())
            raise ValidationError(ex)
