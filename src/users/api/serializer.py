from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.core.exceptions import ValidationError


from django.contrib.auth.models import User
from ..models import*
from address.api.serializer import AddressSerializer

from .utils import*
import traceback
import logging
from kreedo.conf.logger import*
from django.contrib.auth.models import Permission, Group
from group.api.serializer import*
from group.models import*

""" Create Log for Serializer"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("Serailizer CAlled ")


""" Role Model Serializer """


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        depth = 2


""" User Type Serializer """


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'


""" Auth User Serializer """


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_active']


""" UserDetail Serializer """


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')


""" User Detail List Serializer """


class UserDetailListSerializer(serializers.ModelSerializer):
    user_obj = AuthUserSerializer()
    reporting_to = SerializerMethodField()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 1

    def get_reporting_to(self, obj):
        print("@@@@@@@@", obj)
        try:
            reporting_obj = ReportingTo.objects.filter(user_detail=obj).first()
            if reporting_obj == None:
                return {}
            return ReportingToListSerializer(reporting_obj).data
        except Exception as e:
            print(e)
            return None


""" User Detail List Serializer """


class UserDetailListForAcademicSessionSerializer(serializers.ModelSerializer):
    user_obj = AuthUserSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        # depth = 1


""" UserDetailListForSectionSubjectSerializer List Serializer """


class UserDetailListForSectionSubjectSerializer(serializers.ModelSerializer):
    user_obj = AuthUserSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 1


""" User Role Serializer"""


class SchoolUserRoleSerializers(serializers.ModelSerializer):
    user = UserDetailListForSectionSubjectSerializer()

    class Meta:
        model = UserRole
        fields = '__all__'
        depth = 2


""" Reporting To  Serializer """


class ReportingToSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingTo
        fields = '__all__'


""" Reporting To  Serializer """


class ReportingToListSerializer(serializers.ModelSerializer):
    reporting_to = UserDetailListForAcademicSessionSerializer()

    class Meta:
        model = ReportingTo
        fields = '__all__'
        depth = 1


class ReportingToListByUserDetailSerializer(serializers.ModelSerializer):
    reporting_to = UserDetailListForAcademicSessionSerializer()

    class Meta:
        model = ReportingTo
        fields = ['id', 'reporting_to', 'user_role']
        depth = 1


""" User Role Serializer"""


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

    def create(self, validated_data):

        print("User Role Called--------->", validated_data)
        return UserRole.objects.create(**validated_data)


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserRoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class ReportingToCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingTo
        fields = '__all__'

    def create(self, validated_data):
        try:

            reporting_qs = ReportingTo.objects.create(**validated_data)
            """ Role update in User Detail """
            user_detail = UserDetail.objects.get(
                user_obj=validated_data.get('user_detail', None))

            role_id = validated_data.get('user_role', None)
            user_detail.role.add(role_id)
            user_detail.save()
            print("SAVE ROLE")

            """ User Role Creation """
            role_serializer = UserRoleCreateSerializer(
                data=self.context['role_detail'])
            if role_serializer.is_valid():
                role_serializer.save()
            else:
                raise ValidationError(role_serializer.errors)
            return reporting_qs
        except Exception as ex:
            print("ERROR SERIALIZER", ex)
            raise ValidationError(ex)


class ReportingToUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingTo
        fields = '__all__'


""" User Register API """


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        try:
            instance = super(UserRegisterSerializer,
                             self).to_representation(instance)
            """ Update details in RESPONSE """

            instance['user_detail'] = self.context['user_detail_serializer_data']

            instance['user_role'] = self.context['user_role']

            return instance
        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())

    def create(self, validated_data):
        try:
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            password = validated_data['password']
            email = validated_data['email']
            auth_user_created = False
            address_created = False
            user_role_created = False

            """ Validate Email and Password"""
            try:
                email_password = validate_auth_user(email, password)
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
                validated_data['username'] = username
            except ValidationError:
                raise ValidationError("Failed to genrate username")

            """ Creating Auth User and User detail """
            try:
                if User.objects.filter(email=validated_data['email']).exists():
                    raise ValidationError("Email is already Exists")
                else:
                    """ Create User """
                    user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], first_name=first_name,
                                                    last_name=last_name, is_active=False)
                    user.set_password(password)
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

                        """ send User Detail Funation """
                        send_user_details(user, user_detail_serializer.data)

                        school_id = self.context['user_detail_data']['school']
                        print("School--->", school_id)
                        if school_id is not None:
                            print("Succes", school_id)
                            role_id = self.context['user_detail_data']['role']
                            user_role = {
                                "user": user_detail_serializer.data['user_obj'],
                                "role": role_id[0],
                                "school": school_id
                            }

                            user_role_serializer = UserRoleSerializer(
                                data=dict(user_role))
                            if user_role_serializer.is_valid():
                                user_role_serializer.save()

                                self.context.update({
                                    "user_role": user_role_serializer.data
                                })
                                return user
                            else:
                                raise ValidationError(
                                    user_role_serializer.errors)
                        else:

                            return user

                    else:
                        logger.info(user_detail_serializer.errors)
                        logger.debug(user_detail_serializer.errors)
                        raise ValidationError(user_detail_serializer.errors)

            except Exception as ex:
                # user_id = user.id

                # user_obj = User.objects.get(pk=user_id)
                # user_obj.delete()

                logger.info(ex)
                logger.debug(ex)
                raise ValidationError(ex)

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)


""" Email verify Serializer """


class UserEmailVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'is_active']

    def to_representation(self, instance):

        instance = super(UserEmailVerifySerializer,
                         self).to_representation(instance)

        instance['mail_t'] = self.context['mail_t']

        return instance

    def validate(self, validated_data):
        try:
            uidb64 = self.context['user_token_detail']['uidb64']
            token = self.context['user_token_detail']['token']

            assert uidb64 is not None and token is not None  # checked by URLconf
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            try:
                if user is not None and default_token_generator.check_token(user, token):

                    user.is_active = True
                    user.userdetail.email_verified = True
                    user.save()
                    user.userdetail.save()
                    user_obj = User.objects.get(pk=uid)
                    mail_t = verified_user_mail(
                        user_obj.first_name, user_obj.email)

                    mail = "Your email has been verified"

                    self.context.update({"mail_t": mail})
                    return mail
                else:
                    raise ValidationError(
                        "The reset password link is no longer valid.")
            except Exception as ex:
                raise ValidationError("Unable to confirm password")
        except Exception as ex:

            raise ValidationError("Unable to confirm password")


""" User Login Serialzer """


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        try:

            instance = super(UserLoginSerializer,
                             self).to_representation(instance)
            instance['token'] = self.context['token']

            return instance
        except Exception as ex:
            raise ValidationError(ex)

    def validate(self, validated_data):
        try:
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
                            user_detail_serializer = UserDetailSerializer(
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
                logger.info(ex)
                logger.debug(ex)
                raise ValidationError(ex)

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)


""" FORGET PASSWORD"""


class UserForgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active']

    def to_representation(self, instance):
        try:
            instance = super(UserForgetSerializer,
                             self).to_representation(instance)

            instance['data'] = self.context['data']
            return instance

        except Exception as ex:
            raise ValidationError(ex)

    def validate(self, validated_data):
        try:
            try:
                email_id = validated_data.pop('email')

                user_obj = User._default_manager.filter(
                    email=email_id, is_active=True).first()

            except Exception as ex:
                raise ValidationError(
                    "This email ID is not linked to any account. Please check again.")

            try:
                user_detail_obj = UserDetail.objects.get(user_obj=user_obj)

            except Exception as ex:
                raise ValidationError(
                    "This email ID is not linked to any account. Please check again.")

            try:
                # Generate password reset token link and send  email
                generate_user_activation_link_response = generate_user_activation_link(
                    user_obj, user_detail_obj, False)

                if generate_user_activation_link_response["isSuccess"] is True:

                    self.context.update({"data": "Token Sent to user"})
                    data = 'Token Sent to user'
                    return validated_data
                else:
                    raise ValidationError("Failed to send Token to user")

            except Exception as ex:
                logger.info(ex)
                logger.debug(ex)
                raise ValidationError(
                    "This email ID is not linked to any account. Please check again.")

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)


""" CHANGE PASSWORD """


class UserChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active']

    def to_representation(self, instance):
        instance = super(UserChangePasswordSerializer,
                         self).to_representation(instance)
        instance['message'] = self.context['message']
        return instance

    def validate(self, validated_data):
        username = self.context['password_detail']['username']
        old_password = self.context['password_detail']['old_password']
        new_password = self.context['password_detail']['new_password']

        try:
            """ authenticate password and username """
            try:

                user = authenticate_password(
                    username=username, old_password=old_password)
            except Exception as ex:
                raise serializers.ValidationError(
                    "Old Password is not Matched")

            """ Password set """
            try:
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    data = 'Password has been Changed'
                    self.context.update(
                        {"message": 'Password has been Changed'})
                    return validated_data
                else:
                    raise serializers.ValidationError(
                        'User Credentials incorrect')
            except Exception as ex:
                raise serializers.ValidationError('User Credentials incorrect')

        except Exception as ex:

            raise serializers.ValidationError("Old Password is not Matched")


class User_Password_Reseted_Mail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'is_active']

    def to_representation(self, instance):
        instance = super(User_Password_Reseted_Mail_Serializer,
                         self).to_representation(instance)

        instance['data'] = self.context['data']

        return instance

    def validate(self, validated_data):
        try:

            uidb64 = self.context['user_token_detail']['uidb64']
            token = self.context['user_token_detail']['token']

            assert uidb64 is not None and token is not None  # checked by URLconf
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User._default_manager.get(pk=uid)

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            try:
                if user is not None and default_token_generator.check_token(user, token):

                    generate_reset_password_link_response = generate_reset_password_link(
                        user)

                    if generate_reset_password_link_response:

                        self.context.update(
                            {"data": generate_reset_password_link_response})
                        data = 'Token Sent to user'
                        return validated_data
                    else:
                        raise ValidationError("Failed to send Token to user")

                    return validated_data
                else:
                    raise ValidationError(
                        "The reset password link is no longer valid.")
            except Exception as ex:
                raise ValidationError(ex)

        except Exception as ex:
            raise ValidationError(ex)


""" RESET PASSWORD """


class Reset_Password_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'is_active']

    def to_representation(self, instance):
        instance = super(Reset_Password_Serializer,
                         self).to_representation(instance)

        instance['data'] = self.context['data']

        return instance

    def validate(self, validated_data):
        try:

            uidb64 = self.context['user_token_detail']['uidb64']
            token = self.context['user_token_detail']['token']
            password = self.context['password_detail']['password']
            confirm_password = self.context['password_detail']['confirm_password']

            assert uidb64 is not None and token is not None  # checked by URLconf
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User._default_manager.get(pk=uid)

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            try:

                if user is not None and default_token_generator.check_token(user, token):

                    if password == confirm_password:
                        new_password = confirm_password
                        user.set_password(new_password)
                        user.is_active = True
                        user.userdetail.email_verified = True
                        user.save()
                        user.userdetail.save()
                        user_obj = User.objects.get(pk=uid)
                        mail_t = password_reseted_mail(
                            user_obj.first_name, user_obj.email)

                        data = "Password has been reset."
                        self.context.update({"data": data})
                        return validated_data
                    else:
                        raise ValidationError(
                            "Confirm Password Does not match")
                else:
                    raise ValidationError(
                        "The reset password link is no longer valid.")
            except Exception as ex:
                raise ValidationError(ex)

        except Exception as ex:
            raise ValidationError(ex)


class UserRoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
        depth = 2


class UserRoleListForSchoolSerializer(serializers.ModelSerializer):
    user = UserDetailListForAcademicSessionSerializer()

    class Meta:
        model = UserRole
        fields = '__all__'
        depth = 1


class SchoolListByUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['school']
        depth = 2


""" Logged In User Serializer """


class LoggedInUserSerializer(serializers.ModelSerializer):

    user_obj = AuthUserSerializer()

    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')
        depth = 3

    def to_representation(self, obj):
        from session.api.serializer import AcademicSessionListSerializer
        serialized_data = super(
            LoggedInUserSerializer, self).to_representation(obj)
        user_obj_id = serialized_data.get('user_obj')

        user_id = user_obj_id.get('id')
        if UserRole.objects.filter(user=user_id).exists():
            user_role_data = UserRole.objects.filter(user=user_id)
            user_role_data_serializer = UserRoleListSerializer(
                user_role_data, many=True)
            serialized_data['user_role_data'] = user_role_data_serializer.data
        if AcademicSession.objects.filter(class_teacher=user_id).exists():
            acadamic_session_serializer = AcademicSessionListSerializer(
                AcademicSession.objects.filter(class_teacher=user_id), many=True)
            serialized_data['class_teacher_data'] = acadamic_session_serializer.data
        return serialized_data


""" Update user Serializer """


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_active']


""" Add user Serializer """


class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def to_representation(self, instance):
        try:
            instance = super(AddUserSerializer,
                             self).to_representation(instance)
            """ Update details in RESPONSE """
            print("self.context['user_detail']", self.context)
            instance['id'] = self.context['id']

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
                username = create_unique_username()
                validated_data['username'] = username

            except ValidationError:
                raise ValidationError("Failed to genrate username")

            """ Genrate Password """
            try:
                genrated_password = get_random_string(8)
            except Exception as ex:
                raise ValidationError("Failed to Genrate Password")

            try:
                if User.objects.filter(email=validated_data['email']).exists():
                    raise ValidationError("Email is already Exists")
                else:
                    """ Create User """
                    user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], first_name=first_name,
                                                    last_name=last_name, is_active=True)
                    user.set_password(genrated_password)
                    user.save()
                    auth_user_created = True

                    self.context['user_details_data']['user_obj'] = user.id

                    """ Pass request data of User detail Serializer"""

                    user_detail_serializer = UserDetailSerializer(
                        data=self.context['user_details_data'])
                    if user_detail_serializer.is_valid():
                        user_detail_serializer.save()

                        # self.context.update(
                        #     {"user_detail": user_detail_serializer.data})
                        """ send temprorary password mail """
                        send_temprorary_password_mail(
                            user, user_detail_serializer.data, genrated_password)

                    else:
                        raise ValidationError(user_detail_serializer.errors)
                    role = self.context['user_details_data']['role'][0]
                    print("@@@@@@@@@@@@@@@", role)
                    user_role = {
                        "user": user_detail_serializer.data['user_obj'],
                        "role": role,
                        "school": self.context['reporting_to']['school']
                    }
                    print("user_role------------>", user_role)
                    user_role_serializer = UserRoleSerializer(
                        data=dict(user_role))
                    if user_role_serializer.is_valid():
                        user_role_serializer.save()

                        # self.context.update({
                        #     "user_role": user_role_serializer.data
                        # })

                    else:
                        print("ERROR------------>",
                              user_role_serializer.errors)
                        raise ValidationError(user_role_serializer.errors)

                    if "reporting_to" in self.context:
                        self.context['reporting_to']['user_detail'] = user_detail_serializer.data['user_obj']

                        """ pass request data of Reporting to serializer"""
                        reporting_to_serializers = ReportingToSerializer(
                            data=self.context['reporting_to'])
                        if reporting_to_serializers.is_valid():
                            reporting_to_serializers.save()
                            # self.context.update(
                            #     {"reporting_to": reporting_to_serializers.data})

                        else:
                            raise ValidationError(
                                reporting_to_serializers.errors)
                    user_data = {
                        "user_obj": user.id
                    }
                    self.context.update({
                        "id": user.id
                    })
                    return user_data

            except Exception as ex:
                logger.info(ex)
                logger.debug(ex)
                raise ValidationError(ex)

        except Exception as ex:
            print("errror", ex)

            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)


""" Create parent serializer """


class ParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        """ Genrate Username """
        try:
            username = create_unique_username()
            validated_data['username'] = username
        except ValidationError:
            raise ValidationError("Failed to genrate username")

        user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'], first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'], is_active=True)
        return user


""" PArent detail serailizer """


class ParentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'


"""teachers serializer"""


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'email', 'first_name', 'last_name']


class ReportingToRoleSerializer(serializers.ModelSerializer):
    user = UserDetailListForAcademicSessionSerializer()

    class Meta:
        model = UserRole
        fields = '__all__'
        depth = 1
