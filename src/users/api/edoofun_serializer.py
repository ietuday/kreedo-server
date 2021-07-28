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

""" Auth User Serializer """

class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','is_active']


class AccountUserSerializer(serializers.ModelSerializer):

    user_obj = AuthUserSerializer()
    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 3
    
    
   

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


""" User Login Serialzer """


class EdoofunUserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        try:

            instance = super(EdoofunUserLoginSerializer,
                             self).to_representation(instance)
            instance['token'] = self.context['token']

            return instance
        except Exception as ex:
            raise ValidationError(ex)

    def validate(self, validated_data):
        try:
            print("validated_data", validated_data)
            email = validated_data.pop('email')
            password = validated_data.pop('password')

            """ validate email and password """
            try:
                email_password = validate_auth_user(email, password)
            except Exception as ex:
                raise ValidationError("Email and Password is required")

            """ get username"""
            try:

                if email is not None:

                    username = User.objects.get(
                        email=email, is_active=True).username
                    print("username-", username)
                else:
                    raise ValidationError("Email is required")
            except Exception as ex:

                raise ValidationError("Invalid Credentials, Try Again")

            """ authenticate username and password """
            try:
                if username and password is not None:

                    auth_user = authenticate_username_password(
                        username, password)
                else:
                    raise ValidationError("Credentials is required")
            except Exception as ex:
                raise ValidationError("Credentials is required")

            try:
                if auth_user is not None:
                    if auth_user.is_active:
                        try:
                            user_detail = UserDetail.objects.get(
                                user_obj=auth_user)
                            print("user_detail", user_detail)
                            user_detail_serializer = UserDetailsSerializer(
                                user_detail)
                            token = genrate_token(auth_user)
                            self.context.update({"token": token})
                            data = "Login Successful"
                            return data
                        except Exception as ex:
                            raise ValidationError(
                                'Some issue in user detail.Please Check')
                    else:
                        raise ValidationError(
                            "Sorry, this account is deactivated")
                else:
                    raise ValidationError(
                        "Login failed ,Invalid Username and Password")

            except Exception as ex:
                print("ERROr-----11", ex)
                print("TRACEBACK-------1", traceback.print_exc())
                logger.info(ex)
                logger.debug(ex)
                raise ValidationError(ex)

        except Exception as ex:
            print("ERROr-----", ex)
            print("TRACEBACK-------", traceback.print_exc())
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)


""" User Role Serializer"""


class SchoolUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
        depth = 1


""" Create parent serializer """


class EdoofunParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

    def to_representation(self, obj):
        try:
            serialized_data = super(
            EdoofunParentSerializer, self).to_representation(obj)
            
            return self.context

        except Exception as ex:
            print("Error-------", ex)
            print("TRACEBACK-----------", traceback.print_exc())
        

    def create(self, validated_data):
        """ Genrate Username """
        try:
            username = create_username()
            validated_data['username'] = username
        except ValidationError:
            raise ValidationError("Failed to genrate username")

        if User.objects.filter(email=validated_data['email']).exists():
            user_obj_qs = User.objects.filter(email=validated_data['email'])[0]
            self.context.update({"user_obj":user_obj_qs.id,"msg":"user exist"})
            return user_obj_qs
        else:
            user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'], is_active=True)
            
            self.context.update({"user_obj":user.id,"msg":"user create"})
            return user
            


""" PArent detail serailizer """


class EdoofunParentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'


    def create(self, validated_data):
        print("validated_data-------->", validated_data)
        if UserDetail.objects.filter(user_obj=validated_data['user_obj']).exists():
            user_detail_qs = UserDetail.objects.filter(user_obj=validated_data['user_obj'])[0]
            print("user_detail_qs----",user_detail_qs)
            return user_detail_qs
        else:
            user_detail_qs = super(EdoofunParentDetailSerializer, self).create(validated_data)

            return user_detail_qs






""" Update secret pin Serializer """

""" CHANGE PIN """
class UserChangePinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields =['secret_pin']

    def to_representation(self, instance):
        instance = super(UserChangePinSerializer, self).to_representation(instance)
        instance['data'] = self.context['data']
        return instance

    def validate(self, validated_data):
        print("self----------->", self)
        username=self.context['parent_detail']['username']
        email = self.context['parent_detail']['email']
        old_pin=self.context['parent_detail']['old_pin']
        new_pin=self.context['parent_detail']['new_pin']

        try:
            """ authenticate password and username """
            try:
                            
                user = user_obj = User._default_manager.filter(username=username, is_active=True).first()
         
            except Exception as ex:
                raise serializers.ValidationError("User is not Authorized")
            """ Password set """
            try:
                if user is not None:
                    if UserDetail.objects.filter(user_obj=user,secret_pin=old_pin).exists():
                        user_detail_qs = UserDetail.objects.get(user_obj=user,secret_pin=old_pin)
                        user_detail_qs.secret_pin = new_pin
                        user_detail_qs.save()
                        data = "PIN has been reset."
                        self.context.update({"data":data})
                        return validated_data
                    else:
                        raise ValidationError("Old pin is not Matched")
                  
                else:
                    raise serializers.ValidationError('User is not Authorized')
            except Exception as ex:
                raise serializers.ValidationError(ex)
            
        except Exception as ex:
            print("EROR", ex)
            print("TRaceback-------", traceback.print_exc())
         
            raise serializers.ValidationError(ex)


        
""" ParentDetails Serializer """
from child.models import*
from child.api.edoofun_serializer import*
class ParentDetailSerializer(serializers.ModelSerializer):

    user_obj = AuthUserSerializer()
    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 3

    def to_representation(self, obj):
        serialized_data = super(
            ParentDetailSerializer, self).to_representation(obj)
        print("serialized_data",serialized_data['user_obj']['id'])
        user_id = serialized_data['user_obj']['id']

        child_qs = Child.objects.filter(parent=user_id)
        if child_qs:
            child_qs_serializer = ChildListParentSerializer(child_qs,many=True)
            print("child_qs----",child_qs)
            serialized_data['child_list'] = child_qs_serializer.data
        return serialized_data



""" AccountListtSerializer List Serializer """
class AccountListForSerializer(serializers.ModelSerializer):
    user_obj = AuthUserSerializer()
    
    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires','address')
        depth = 1



""" AccountListtSerializer List Serializer """
class LicenceForSerializer(serializers.ModelSerializer):
    user_obj = AuthUserSerializer()
    
    class Meta:
        model = UserDetail
        fields = ['user_obj','phone']
        depth = 1


class SchoolUserRoleSerializers(serializers.ModelSerializer):
    user = AccountListForSerializer()
    class Meta:
        
        model = UserRole
        fields = ['user', 'school']
        depth = 2


class UserListBySchoolSerializers(serializers.ModelSerializer):
    user = AccountListForSerializer()
    class Meta:
        
        model = UserRole
        fields = ['user']
        depth = 1



""" User Detail List Serializer """
class UserDetailListSerializer(serializers.ModelSerializer):
    user_obj = AuthUserSerializer()
    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        # depth = 1
    
