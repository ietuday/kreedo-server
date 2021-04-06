from rest_framework import serializers

from django.contrib.auth.models import User
from ..models import*
from address.api.serializer import AddressSerializer
from .utils import*
import traceback

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


""" User Register API """
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id','email','first_name','last_name','password','is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        instance = super(UserRegisterSerializer, self).to_representation(instance)
        """ Update details in RESPONSE """
        instance['user_detail'] = self.context['user_detail_serializer']
        instance['user_detail']['address'] = self.context['address_detail_serializer']
        return instance
    
    def validate(self,validated_data):
        try:
            
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            password = validated_data['password']
            email = validated_data['email']
            print("email",email)

            """ Validate Email and Password"""
            try:
                email_password = validate_auth_user(email,password)
            except ValidationError:
                raise serializers.ValidationError("Email and Password is required")

            """ Validate Email """
            try:
                if not email:
                    raise serializers.ValidationError("Email is required")
                else:
                    email = user_validate_email(email)
                    print("email", email)
                    if email is True:
                       validated_data['email'] = validated_data['email'].lower().strip()
                    else:
                       raise serializers.ValidationError("Enter a valid email address")
            except ValidationError:
                raise serializers.ValidationError("Enter a valid email address")
            
            """ Genrate Username """
            try:
                username = create_unique_username()
                print("username",username)
                validated_data['username'] = username
            except ValidationError:
                raise serializers.ValidationError("Failed to genrate username")

            """ Creating Auth User and User detail """
            try:
                if User.objects.filter(email=validated_data['email']).exists():
                    raise ValidationError("Email is already Exists")
                else:               
                    """ Create User """
                    user = User.objects.create_user(email=validated_data['email'] , username=validated_data['username'], first_name=first_name,
                            last_name=last_name,is_active=False)
                    user.set_password(password)
                    user.save()
                    self.context['user_detail_data']['user_obj'] = user.id

                    """ Pass request data of User detail"""
                    print("self.context['user_detail_data'])",self.context['user_detail_data'])
                    user_detail_serializer = UserDetailSerializer(data = self.context['user_detail_data'])
                    if user_detail_serializer.is_valid():
                        user_detail_serializer.save()

                        self.context.update({"user_detail_serializer": user_detail_serializer.data})
                        
                        """ send User Detail Funation """
                        send_user_details(user,user_detail_serializer.data)

                        # ADDRESS DETAIL
                        address_serializer = AddressSerializer(data = self.context['address_detail'])
                        if address_serializer.is_valid():
                            address_serializer.save()
                            print("address_serializer.data------------->", address_serializer.data['id'])

                            user_detail_serializer['address'] = address_serializer.data['id']
                            print("validated_data['address']",validated_data['address'])
                            user_address = user_detail_serializer(data=user_detail_serializer['address'])
                            user_address.save()

                            self.context.update({"address_detail_serializer":address_serializer.data})
                        else:
                            raise serializers.ValidationError("address",address_serializer.errors)
                    else:
                        raise serializers.ValidationError("user detail",user_detail_serializer.errors)

            except Exception as ex:
                raise serializers.ValidationError("Failed to save User details")
            
        except Exception as ex:
            print("error------------", ex)
            print("traceback", traceback.print_exc())
    
    
    
    # def create(self,validated_data):
    #     print("CREATE@@@@@@@@@@@@@@@@@@", validated_data)
    