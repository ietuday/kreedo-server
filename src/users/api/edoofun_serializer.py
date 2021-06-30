from kreedo.conf.logger import*
import logging
import traceback
from .edoofun_utils import*
from address.api.serializer import AddressSerializer
from ..models import*
from rest_framework import serializers
"""
    Django Files
"""
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError)
"""
    App Files
"""


""" Create Log for Edoo-Fun  Serializer"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("Serailizer CAlled ")


""" Register Parent Serializer """


class RegisterParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            print("@@@@@@@@ User", validated_data)
            # print("SELF-----------------", self)
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            email = validated_data['email']
            auth_user_created = False
            address_created = False
            user_role_created = False

            """ Validate Email """
            try:
                if not email:
                    raise ValidationError("Email is required")
                else:

                    email = user_validate_email(email)
                    if email is True:
                        print("Email TRUE")
                        validated_data['email'] = validated_data['email'].lower(
                        ).strip()
                    else:
                        raise ValidationError(
                            "Enter a valid email address")
            except ValidationError:
                raise ValidationError(
                    "Enter a valid email address")
            try:
                if User.objects.filter(email=validated_data['email']).exists():
                    if UserDetail.objects.filter(phone=self.context['user_detail_data']['phone']).exists():
                        print("Provide Correct Registered Number.")
                        raise ValidationError(
                            "Provide Correct Registered Number.")
                raise ValidationError("Provide Correct Registered Number.")
            except Exception as ex:
                raise ValidationError(ex)

            try:
                user_email = User.objects.filter(email=validated_data['email'])

                if UserDetail.objects.filter(phone=self.context['user_detail_data']['phone']).exists():
                    print(
                        "Phone already regsitered for another user provide different no")
            except Exception as ex:
                raise ValidationError(ex)

            """ Genrate Username """
            try:
                username = create_unique_username()
                print("username", username)
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
                    raise ValidationError("Email is already Exists")
                else:
                    """ Create User """
                    user = User.objects.create_user(email=validated_data['email'], username=username, first_name=first_name,
                                                    last_name=last_name, is_active=False)
                    user.set_password(genrated_password)
                    user.save()
                    auth_user_created = True
                    self.context['user_detail_data']['user_obj'] = user.id

                    """ Pass request data of User detail"""

                    user_detail_serializer = UserDetailSerializer(
                        data=self.context['user_detail_data'])
                    if user_detail_serializer.is_valid():
                        user_detail_serializer.save()
                        self.context.update(
                            {"user_detail_serializer_data": user_detail_serializer.data})
                        return user

                    else:
                        logger.info(user_detail_serializer.errors)
                        logger.debug(user_detail_serializer.errors)
                        raise ValidationError(user_detail_serializer.errors)

            except Exception as ex:

                logger.info(ex)
                logger.debug(ex)
                raise ValidationError(ex)

        except Exception as ex:
            print("SERIALIZER---------Error", ex)
            print("TRACEBACK", traceback.print_exc())
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)
