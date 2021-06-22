from rest_framework import serializers
""" 
    Django Files 
"""
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
""" 
    App Files  
"""
from ..models import*
from address.api.serializer import AddressSerializer
from .utils import*
import traceback
import logging
from kreedo.conf.logger import*



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
            print("validated_data------>",validated_data)
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            email = validated_data['email']
            auth_user_created = False
            address_created = False
            user_role_created = False


            """ Validate Email """
            try:
                email_password = validate_auth_user(email)
            except ValidationError:
                raise ValidationError(
                    "Email and Password is required")

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
                username = create_unique_username()
                print("username", username)
                validated_data['username'] = username
            except ValidationError:
                raise ValidationError("Failed to genrate username")
                     
            """ Genrate Password """
            try:
                genrated_password = get_random_string(8)
                print("genrated_password----------->", genrated_password)
            except Exception as ex:
                raise ValidationError("Failed to Genrate Password")


            
 
        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            return Response(ex)