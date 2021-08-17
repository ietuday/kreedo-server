"""
    DJANGO LIBRARY IMPORT
"""

from passlib.hash import pbkdf2_sha256
from kreedo.settings import AWS_SNS_CLIENT, EMAIL_HOST_USER
from schools.models import*
from schools.api.edoofun_serializer import*
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework .generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from ..models import*
from .filters import*
from .edoofun_serializer import*
from kreedo.general_views import Mixins, GeneralClass
from users.api.custum_storage import FileStorage

import traceback
import datetime
import random

from kreedo.conf import logger
from kreedo.conf.logger import CustomFormatter
import logging
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

""" Logger Function """


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")


"""  Register Parent """


class RegisterParent(ListCreateAPIView):
    def post(self, request):
        try:
            user_data = {
                "username": "test",
                "first_name": request.data.get('first_name', None),
                "last_name": request.data.get('last_name', None),
                "email": request.data.get('email', None)
            }
            role_id = Role.objects.filter(name="Parent")[0].id
            type_id = UserType.objects.filter(name='School Users-Parent')[0].id
            print("role-------", role_id)
            user_detail_data = {
                "photo": request.data.get('photo', None),
                "phone": request.data.get('phone', None),
                "relationship_with_child": request.data.get('relationship_with_child', None),
                "role": [role_id],
                "type": type_id,
                "is_platform_user": request.data.get('is_platform_user', None)
            }

            print("user_detail_data----------", user_detail_data)

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"user_data": user_data, "user_detail_data": user_detail_data})

            user_detail_serialzer = RegisterParentSerializer(
                data=dict(user_data), context=context)

            if user_detail_serialzer.is_valid():
                user_detail_serialzer.save()

                context = {"isSuccess": True, "message": "Parent created sucessfully",
                           "error": "", "data": user_detail_serialzer.data, "status": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {"isSuccess": False, "message": "Issue in Parent Creation",
                           "error": user_detail_serialzer.errors, "data": "", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print("Error------>", ex)
            print("TRACEBACK---------->", traceback.print_exc())

            context = {"isSuccess": False, "message": "Issue in Parent Creation", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" login Register """


class LoginUserBasedOnEmailD(ListCreateAPIView):
    model = User

    def post(self, request):
        try:

            user_data_serializer = EdoofunUserLoginSerializer(
                data=request.data)
            if user_data_serializer.is_valid():
                context = {'isSuccess': True, 'message': "Login Successfull",
                           'data': user_data_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
                # return Response(user_data_serializer.data, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, "error": user_data_serializer.errors['non_field_errors'][0],
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            context = {'isSuccess': False, 'message': "Something went wrong",
                       'error': ex, "statusCode": status.HTTP_400_BAD_REQUEST}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


""" login with Contact Number """


class LoginUserBasedOnContactNumber(ListCreateAPIView):

    def post(self, request):
        try:
            user_detail_data = {
                "phone": request.data.get('phone', None)
            }

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"user_detail_data": user_detail_data})
            user_data_serializer = EdoofunUserLoginContactSerializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():
                context = {'isSuccess': True, 'message': "Login Successfull",
                           'data': user_data_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
                # return Response(user_data_serializer.data, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, "error": user_data_serializer.errors['non_field_errors'][0],
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            context = {'isSuccess': False, 'message': "Something went wrong",
                       'error': ex, "statusCode": status.HTTP_400_BAD_REQUEST}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


"""Get All ACCOUNT """


class GetAllAccounts(ListCreateAPIView):
    def post(self, request):

        try:
            print("@@@@@@@@@@@@", request.data)
            if request.data['type'] == 'account_id':
                user_role_qs = UserRole.objects.filter(
                    user=request.data.get('account_id', None))
                user_role_qs_serializer = SchoolUserRoleSerializers(
                    user_role_qs, many=True)

                context = {'isSuccess': True, 'message': "School List by Account Id",
                           'data': user_role_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)

            elif request.data['type'] == 'school_id':
                print("35")

                school_qs = School.objects.filter(
                    id=request.data.get('school_id', None))
                print("school_qs", school_qs)
                school_qs_serializer = SchoolListSerializer(
                    school_qs, many=True)

                context = {'isSuccess': True, 'message': "School Detail by School Id",
                           'data': school_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            elif request.data['type'] == 'all':
                roles = Role.objects.get(name='School Account Owner')
                roles = roles.id

                user_obj = UserDetail.objects.filter(role=roles)
                if user_obj:

                    user_obj_serializer = AccountUserSerializer(
                        user_obj, many=True)

                    context = {'isSuccess': True, 'message': "Accounts List",
                               'data': user_obj_serializer.data, "statusCode": status.HTTP_200_OK}
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context = {'isSuccess': False, 'message': "Accounts List Not Found",
                               'data': user_obj_serializer.errors, "statusCode": status.HTTP_404_NOT_FOUND}
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print("@@@@@@@@", ex)
            print("TRACEBACK---", traceback.print_exc())
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""  Get UsersBasedOnSchoolID """


class GetUsersBasedOnSchoolID(ListCreateAPIView):
    def get(self, request, pk):
        try:
            role_qs = Role.objects.get(name='School Account Owner').id

            user_role = UserRole.objects.filter(
                school=pk).exclude(role=role_qs)
            if user_role:
                user_role_serializer = UserListBySchoolSerializers(
                    user_role, many=True)

                context = {'isSuccess': True, 'message': "User List By School",
                           'data': user_role_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, 'message': "User List By School Not Found",
                           'data': " ", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("@@@@@@@@", ex)
            print("TRACEBACK---", traceback.print_exc())
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Update Secret  PIN  For Parent """


class UpdateSecretPinForParent(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            parent_detail = {
                "username": request.user.username,
                "email": request.data.get('parent_email', None),
                "old_pin": request.data.get('old_pin', None),
                "new_pin": request.data.get('new_pin', None)
            }

            context = super().get_serializer_context()
            context.update({"parent_detail": parent_detail})
            user_qs_serializer = UserChangePinSerializer(
                data=request.data, context=context)
            if user_qs_serializer.is_valid():

                context = {'isSuccess': True, 'message': "Pin changed Successfully",
                           "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {'isSuccess': False, 'message': "User Not Found",
                           'data': " ", "error": user_qs_serializer.errors, "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print("EX", ex)
            print("traceback", traceback)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" GetParentDetails """


class GetParentDetails(ListCreateAPIView):
    def get(self, request, pk):
        try:
            user_qs = UserDetail.objects.filter(user_obj=pk)
            if user_qs:
                user_qs_serializer = ParentDetailSerializer(user_qs, many=True)
                context = {'isSuccess': True, 'message': "Parent Detail", 'data': user_qs_serializer.data,
                           "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, 'message': "Parent Detail Not Found",
                           'data': " ", "error": user_qs_serializer.errors, "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print("EX", ex)
            print("traceback", traceback)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Get List Of Schools BasedOn AccountID """


class SchoolListByUser(GeneralClass, Mixins, ListCreateAPIView):
    model = UserRole
    filterset_class = UserRoleFilter

    def get(self, request, pk):
        try:
            user_school_qs = UserRole.objects.filter(
                user=pk).exclude(school__isnull=True)

            user_school_qs_serializer = SchoolListByUserSerializer(
                user_school_qs, many=True)
            return Response(user_school_qs_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Log in user detail """


@permission_classes((IsAuthenticated,))
class LoggedInUser(ListAPIView):
    def get(self, request):
        try:

            logged_user = request.user
            user_obj_detail = UserDetail.objects.get(pk=logged_user.id)
            user_data = LoggedInUserDetailSerializer(user_obj_detail)
            context = {'isSuccess': True, 'message': "Parent Detail", 'data': user_data.data,
                       "statusCode": status.HTTP_200_OK}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as ex:
            print("ERROR-------", ex)
            print("traceback", traceback)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Set Password """


class SetPassword(CreateAPIView):
    # model = User

    def post(self, request):
        try:

            password_detail = {
                "user_id": request.data.get('user_id', None),
                "new_password": request.data.get('new_password', None),
                "confirm_password": request.data.get('confirm_password', None),

            }
            context = super().get_serializer_context()
            context.update({"password_detail": password_detail})

            user_data_serializer = ParentChangePasswordSerializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():
                print(user_data_serializer.data)
                context = {'isSuccess': True, 'message': "Password has been Changed", "data": user_data_serializer.data, ""
                           "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:

                context = {"error": user_data_serializer.errors, 'isSuccess': False,
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Genrate OTP """


class EdoofunGenerateOTP(ListAPIView):

    def post(self, request):
        try:
            user_obj = UserDetail.objects.filter(
                phone=request.data['phone']).first()

            print("@@@@@@@@@@@@@@@----", user_obj)
            if user_obj == None:
                context = {'error': "This phone number is not linked to any account. Please check again.",
                           'isSuccess': "false", 'message': 'This phone number is not linked to any account. Please check again.'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            random_number = random.randint(100000, 999999)
            print("random_number--------", random_number)
            print("AWS_SNS_CLIENT-@@@@@@---------", AWS_SNS_CLIENT)
            response = AWS_SNS_CLIENT.publish(
                PhoneNumber=request.data['country_code']+request.data['phone'],
                Message='OTP to set your password for your Kreedo account is ' +
                str(random_number) + " .This OTP will expire after 2 minutes",
                Subject='Reset Password',
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'Kreedo'
                    }
                }
            )

            print("RESPONSE-----", response)

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                context = {"isSuccess": False, "message": "Unable to send OTP",
                           "error": " AWS SNS is Unable to send OTP"}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            date_time = datetime.datetime.now()

            hashed_otp_combo = pbkdf2_sha256.hash(
                str(random_number) + str(date_time) + str(user_obj.user_obj))
            print("hashed_otp_combo----", hashed_otp_combo)
            data = {
                "otp": hashed_otp_combo[14:],
                "phone": request.data['phone'],
                "datetime": str(date_time)
            }

            context = {"isSuccess": True, "message": response,
                       "error": "", "data": data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            print("TRACEBACK-----------", traceback.print_exc())

            context = {'error': str(error), 'isSuccess': "false",
                       'message': 'Unable to generate OTP'}
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" OTP VERIFICATION  """


class EdoofunOTPVerification(ListAPIView):

    def post(self, request):
        try:
            user_obj = UserDetail.objects.filter(
                phone=request.data['phone']).first()
            print("user_obj----", user_obj)
            if user_obj == None:
                context = {'error': "User with this phone number does not exist",
                           'isSuccess': "false", 'message': 'User with this phone number does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            date_time = datetime.datetime.strptime(
                request.data['datetime'], "%Y-%m-%d %H:%M:%S.%f")

            if datetime.datetime.now() - date_time >= datetime.timedelta(seconds=140):
                context = {'error': "OTP expired",
                           'isSuccess': "false", 'message': 'OTP expired'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            print("OTP--------", request.data['entered_otp'])
            # hashed_otp_combo = pbkdf2_sha256.hash(str(request.data['entered_otp']) + str(date_time) + str(user_obj.id))
            pbkdf2_sha256.hash(
                str(request.data['entered_otp']) + str(date_time) + str(user_obj.user_obj))

            if pbkdf2_sha256.verify(str(request.data['entered_otp']) + str(date_time) + str(user_obj.user_obj), "$pbkdf2-sha256" + request.data['otp']):
                activation_key = urlsafe_base64_encode(force_bytes(str(user_obj.user_obj.pk))).decode(
                    'utf-8') + '-' + default_token_generator.make_token(user_obj.user_obj)
                link = os.environ.get(
                    'kreedo_url') + '/users/reset_password_confirm/' + activation_key

                # Add activation key and expiration date to user profile
                user_obj.activation_key = activation_key
                user_obj.key_expires = datetime.datetime.strftime(
                    datetime.datetime.now() + datetime.timedelta(minutes=1), "%Y-%m-%d %H:%M:%S")
                user_obj.save()

                data = {
                    "link": link,
                }

                context = {
                    "isSuccess": True, "message": "OTP successfully validated", "error": "", "data": data}
                return Response(context, status=status.HTTP_200_OK)
            context = {'error': "Validation failed",
                       'isSuccess': "false", 'message': 'Failed to validate OTP'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print("@ERROR---------", ex)
            print("TRACEBACK----", traceback.print_exc())
            context = {'error': str(ex), 'isSuccess': "false",
                       'message': 'Unable to validate OTP'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Get all the User list """


# class GetUserList(ListCreateAPIView):
#     def get(self):
#         try:
#             role_qs = aRole.objects.filter(name=d)
#         except Exception as ex:
#             print("@ERROR---------", ex)
#             print("TRACEBACK----", traceback.print_exc())
#             context = {'error': str(ex), 'isSuccess': "false",
#                        'message': 'Unable to validate OTP'}
#             return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
