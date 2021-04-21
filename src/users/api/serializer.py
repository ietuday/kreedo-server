from rest_framework import serializers
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


""" User Type Serializer """


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'


""" Auth User Serializer """

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['id','username','first_name','last_name','email','is_active']

""" UserDetail Serializer """


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        exclude = ('activation_key', 'activation_key_expires')


""" Reporting To  Serializer """


class ReportingToSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingTo
        fields = '__all__'


""" User Role Serializer"""


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

    def create(self, validated_data):
        print("User Role Called--------->", validated_data)
        return UserRole.objects.create(**validated_data)


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
            print("traceback",traceback.print_exc())
            

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
                                raise ValidationError(user_role_serializer.errors)
                        else:
                            return user
                        
                    else:
                        logger.info(user_detail_serializer.errors)
                        logger.debug(user_detail_serializer.errors)
                        raise ValidationError(user_detail_serializer.errors)

            except Exception as ex:
                user_id = user.id
                print('user id------->', user_id)
                user_obj = User.objects.get(pk=user_id)
                user_obj.delete()
                print("user delet")
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
     
        instance = super(UserEmailVerifySerializer, self).to_representation(instance)
        
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
                   
                    mail="Password Has Been Reset"
                    
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
        fields = ['id', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        try:
           
            instance = super(UserLoginSerializer,
                         self).to_representation(instance)
            instance['token'] = self.context['token']
            instance['user_detail'] = self.context['user_detail']

            return instance
        except Exception as ex:
            raise ValidationError(ex)
        

    def validate(self, validated_data):
        try:
            email = validated_data.pop('email')
            password = validated_data.pop('password')

            """ validate email and password """
            try:
                email_password = validate_auth_user(email,password)
            except Exception as ex:
                raise ValidationError("Email and Password is required")
            

            """ get username"""
            try:
                print("email",email)
                if email is not None:
                    print("email--->", email)
                    username = User.objects.get(email = email, is_active=True).username
                    print("username", username)
                else:
                    raise ValidationError("Email is required")
            except Exception as ex:
                
                raise ValidationError("Invalid Credentials, Try Again")

           
            """ authenticate username and password """
            try:
                if username and password is not None:
                   
                    auth_user = authenticate_username_password(username,password)
                else:
                    raise ValidationError("Credentials is required")
            except Exception as ex:
                raise ValidationError("Credentials is required")
            
            
            try:
                if auth_user is not None:
                    if auth_user.is_active:
                        try:
                            user_detail = UserDetail.objects.get(user_obj=auth_user)
                            user_detail_serializer = UserDetailSerializer(user_detail)

                            token = genrate_token(auth_user)
                            
                            self.context.update({"token": token})
                            self.context.update({"user_detail":user_detail_serializer.data})
                            data="Login Successful"
                            
                            return data
                        except Exception as ex:
                            raise ValidationError('Some issue in user detail.Please Check')
                        
                    else:
                        raise ValidationError("Sorry, this account is deactivated")
                else:
                    raise ValidationError("Login failed ,Invalid Username and Password")
                
                
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
        fields =  ['id', 'email', 'first_name', 'last_name', 'is_active']

    def to_representation(self, instance):
        try:
            instance = super(UserForgetSerializer, self).to_representation(instance)

            instance['t'] = self.context['t']
            return instance

        except Exception as ex:
            raise ValidationError(ex)
        

    def validate(self, validated_data):
        try:
            try:
                email_id = validated_data.pop('email')
                
                user_obj = User._default_manager.filter(email = email_id, is_active=True).first()   
                        
            except Exception as ex:
                raise ValidationError("This email ID is not linked to any account. Please check again.")

            try:
                user_detail_obj = UserDetail.objects.get(user_obj=user_obj)
                
            except Exception as ex:
                raise ValidationError("This email ID is not linked to any account. Please check again.")

            try:                
                # Generate password reset token link and send  email
                generate_user_activation_link_response = generate_user_activation_link(user_obj, user_detail_obj,False)
                
                if generate_user_activation_link_response["isSuccess"] is True:
                    
                    self.context.update({"t":generate_user_activation_link_response})
                    data = 'Token Sent to user'
                    return data
                else:
                    raise ValidationError("Failed to send Token to user")
            except Exception as ex:
                logger.info(ex)
                logger.debug(ex)
                raise ValidationError("This email ID is not linked to any account. Please check again.")
        
        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)

""" CHANGE PASSWORD """
class UserChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id', 'email', 'first_name', 'last_name', 'is_active']

    def to_representation(self, instance):
        instance = super(UserChangePasswordSerializer, self).to_representation(instance)
        instance['message'] = self.context['message']
        return instance

    def validate(self, validated_data):
        username=self.context['password_detail']['username']
        old_password=self.context['password_detail']['old_password']
        new_password=self.context['password_detail']['new_password']

        try:
            """ authenticate password and username """
            try:
                            
                user = authenticate_password(username=username,old_password=old_password)
            except Exception as ex:
                raise serializers.ValidationError("Old Password is not Matched")
            
            """ Password set """
            try:
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    data ='Password has been Changed'
                    self.context.update({"message":'Password has been Changed'})
                    return data
                else:
                    raise serializers.ValidationError('User Credentials incorrect')
            except Exception as ex:
                raise serializers.ValidationError('User Credentials incorrect')
            
        except Exception as ex:
         
            raise serializers.ValidationError("Old Password is not Matched")


class User_Password_Reseted_Mail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','first_name', 'last_name', 'is_active']

    def to_representation(self, instance):
        instance = super(User_Password_Reseted_Mail_Serializer, self).to_representation(instance)
        
        instance['mail_t'] = self.context['mail_t']
       
        return instance

    def validate(self,validated_data):
        try:
            
            uidb64 = self.context['user_token_detail']['uidb64']
            token = self.context['user_token_detail']['token']
            password = self.context['password_detail']['password']
            confirm_password = self.context['password_detail']['confirm_password']
            
            
            # password = validated_data.pop('password')
            # confirm_password = validated_data.pop('confirm_password')

            
            assert uidb64 is not None and token is not None  # checked by URLconf
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User._default_manager.get(pk=uid)
              
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            try:
                
                if user is not None and default_token_generator.check_token(user,token):
                    
                    if  password==confirm_password:
                        new_password = confirm_password
                        user.set_password(new_password)
                        user.is_active = True
                        user.userdetail.email_verified = True
                        user.save()
                        user.userdetail.save()
                        user_obj = User.objects.get(pk=uid)
                        mail_t = password_reseted_mail(user_obj.first_name, user_obj.email)
                        self.context.update({"mail_t":'mail_t'})
                        data = "Password has been reset."
                       
                        return data
                    else:
                        raise ValidationError("Confirm Password Does not match")
                else:
                    raise ValidationError("The reset password link is no longer valid.")
            except Exception as ex:
                raise ValidationError(ex)

        except Exception as ex:
            raise ValidationError(ex)  


