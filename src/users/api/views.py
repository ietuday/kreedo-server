"""
    DJANGO LIBRARY IMPORT
"""
import os
from datetime import date
import math as m
import math
import pdb
import csv
import ast
from re import U
from pandas import DataFrame
import json
from .serializer import*
from ..models import*
from .filters import*
from kreedo.general_views import Mixins, GeneralClass
from kreedo.conf.logger import CustomFormatter
import traceback
import datetime
import logging
import pandas as pd


import random
from kreedo.settings import AWS_SNS_CLIENT, EMAIL_HOST_USER
from passlib.hash import pbkdf2_sha256

from rest_framework .generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.decorators import permission_classes
from django.core.exceptions import ValidationError
from django.shortcuts import render
from users.api.custum_storage import FileStorage
from schools.models import*
from schools.api.serializer import*
from package.models import*
from package.api.serializer import*
from session.models import*
from session.api.serializer import*
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("VIEW CAlled ")


# Create your views here.
""" Role List and Create API"""


class RoleListCreate(Mixins, GeneralClass, ListCreateAPIView):
    model = Role
    filterset_class = RoleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoleListSerializer
        if self.request.method == 'POST':
            return RoleSerializer


""" Role Retrive, Update and Delete  API"""


class RoleRetriveUpdateDestroy(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
    model = Role
    serializer_class = RoleSerializer
    filterset_class = RoleFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" User Type List and Create """


class UserTypeListCreate(Mixins, GeneralClass, ListCreateAPIView):
    model = UserType
    serializer_class = UserTypeSerializer
    filterset_class = UserTypeFilter


""" Retrive ,Update and Delete User Type """


class UserTypeRetriveUpdateDelete(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
    model = UserType
    serializer_class = UserTypeSerializer
    filterset_class = UserTypeFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Reporting_to  List and Create API"""


class ReportingToListCreate(Mixins, GeneralClass, ListCreateAPIView):
    model = ReportingTo
    serializer_class = ReportingToSerializer
    filterset_class = ReportingToFilter


""" Reporting to  Retrive, Update and Delete  API"""


class ReportingToRetriveUpdateDestroy(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
    model = ReportingTo
    serializer_class = ReportingToSerializer
    filterset_class = ReportingToFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" User Detail List """


class UserList(Mixins, GeneralClass, ListAPIView):
    model = UserDetail
    serializer_class = UserDetailListSerializer
    filterset_class = UserDetailFilter


class UserRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = UserDetail
    filterset_class = UserDetailFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailListSerializer

        if self.request.method == 'POST':
            return UserDetailSerializer
        if self.request.method == 'PATCH':
            return UserDetailSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" User Register API """


class UserRegister(Mixins, GeneralClass, CreateAPIView):
    def post(self, request):
        try:

            address_detail = {
                "country": request.data.get('country', None),
                "state": request.data.get('state', None),
                "city": request.data.get('city', None),
                "address": request.data.get('address', None),
                "pincode": request.data.get('pincode', None)
            }
            address_created = False
            address_serializer = AddressSerializer(data=address_detail)
            if address_serializer.is_valid():
                address_serializer.save()
                address_created = True

            else:
                print("address_serializer._errors", address_serializer._errors)
                raise ValidationError(address_serializer.errors)

            user_data = {
                "username": "test",
                "password": request.data.get('password', None),
                "first_name": request.data.get('first_name', None),
                "last_name": request.data.get('last_name', None),
                "email": request.data.get('email', None)

            }
            user_detail_data = {
                "phone": request.data.get('phone', None),
                "reason_for_discontinution": request.data.get('reason_for_discontinution', None),
                "relationship_with_child": request.data.get('relationship_with_child', None),
                "role": request.data.get('role', None),
                "type": request.data.get('type', None),
                "school": request.data.get('school', None),
                "address": address_serializer.data['id']

            }

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"user_data": user_data, "user_detail_data": user_detail_data})
            try:
                user_detail = UserRegisterSerializer(
                    data=dict(user_data), context=context)
            except Exception as ex:

                context = {"error": ex,
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)

            if user_detail.is_valid():
                user_detail.save()
                # context = {"message": "User is created successfully. User will get reset password email within 24 hours.",
                #            "data": user_detail.data, "statusCode": status.HTTP_200_OK}

                return Response(user_detail.data, status=status.HTTP_200_OK)
            else:
                logger.debug(
                    user_detail.errors)
                # context = {"error": user_detail.errors,
                #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(user_detail.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            if address_created == True:
                address_id = address_serializer.data['id']
                address_obj = Address.objects.get(pk=address_id)
                address_obj.delete()
            logger.debug(ex)
            # context = {"error": ex,
            #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Email Confirm Verification"""


class EmailConfirmVerify(Mixins, GeneralClass, ListAPIView):
    # model = User
    serializer_class = UserEmailVerifySerializer

    def get(self, request, uidb64, token):
        try:
            user_token_detail = {
                "uidb64": uidb64,
                "token": token
            }
            context = super().get_serializer_context()
            context.update({"user_token_detail": user_token_detail})

            try:
                user_serializar = UserEmailVerifySerializer(
                    data=request.data, context=context)
            except Exception as ex:

                # context = {"error": ex,
                #            "StatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user_serializar.is_valid():

                # context = {"mail_t": user_serializar.data, "message": 'Email Verified',
                #            "statusCode": status.HTTP_200_OK}
                return Response(user_serializar.data, status=status.HTTP_200_OK)
            else:

                # context = {"error": user_serializar.errors,
                #            "StatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(user_serializar.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:

            # context = {"error": ex,
            #            "StatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Login """


class UserLogin(Mixins, CreateAPIView):
    model = User

    def post(self, request):
        try:
            # pdb.set_trace()
            user_data_serializer = UserLoginSerializer(data=request.data)
            if user_data_serializer.is_valid():
                print("####################")
                context = {'isSuccess': True, 'message': "Login Successfull",
                           'data': user_data_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
                # return Response(user_data_serializer.data,status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, "message": user_data_serializer.errors['non_field_errors'][0],
                           "statusCode": status.HTTP_200_OK, 'data': ''}
                return Response(context, status=status.HTTP_200_OK)
                # return Response(user_data_serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            context = {'isSuccess': False, 'message': "Something went wrong",
                       'error': ex, "statusCode": status.HTTP_400_BAD_REQUEST}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
            # return Response(ex,status=status.HTTP_400_BAD_REQUEST)


""" Forget password """


class ForgetPassword(Mixins, GeneralClass, CreateAPIView):
    # model = User

    def post(self, request):
        try:

            user_data_serializer = UserForgetSerializer(data=request.data)

            if user_data_serializer.is_valid():

                # context = {"message": "Token send to user", 'isSuccess': True,
                #            "statusCode": status.HTTP_200_OK}
                # return Response(context)
                return Response(user_data_serializer.data['data'], status=status.HTTP_200_OK)
            else:
                # context = {"error": user_data_serializer.errors, 'isSuccess': False,
                #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                # return Response(context)
                return Response(user_data_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:

            # context = {"error": ex, 'isSuccess': False,
            #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""CHANGE PASSWORD """

# @permission_classes((IsAuthenticated,))


class ChangePassword(Mixins, GeneralClass, CreateAPIView):
    # model = User
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            password_detail = {
                "username": request.user.username,
                "old_password": request.data.get('old_password', None),
                "new_password": request.data.get('new_password', None)
            }
            context = super().get_serializer_context()
            context.update({"password_detail": password_detail})

            user_data_serializer = UserChangePasswordSerializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():

                # context = {"data": user_data_serializer.data,
                #            "statusCode": status.HTTP_200_OK}
                # return Response(context)
                return Response(user_data_serializer.data['message'], status=status.HTTP_200_OK)
            else:

                # context = {"error": user_data_serializer.errors,
                #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(user_data_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            # context = {"error": ex,
            #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Reset Email Confirm """


class ResetPasswordConfirm(Mixins, GeneralClass, CreateAPIView):
    # model = User
    serializer_class = User_Password_Reseted_Mail_Serializer

    def get(self, request, uidb64, token):
        try:
            user_token_detail = {
                "uidb64": uidb64,
                "token": token
            }
            context = super().get_serializer_context()
            context.update({"user_token_detail": user_token_detail})
            user_data_serializer = User_Password_Reseted_Mail_Serializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():
                print("VIEW----", user_data_serializer.data['data'])
                return HttpResponseRedirect(user_data_serializer.data['data'])
                # return Response(user_data_serializer.data['data'], status=status.HTTP_200_OK)
            else:
                print("Error,", user_data_serializer.errors)

                return Response(user_data_serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Rest password """


class ResetPassword(Mixins, GeneralClass, CreateAPIView):
    serializer_class = Reset_Password_Serializer

    def post(self, request, uidb64, token):
        try:
            user_token_detail = {
                "uidb64": uidb64,
                "token": token
            }
            password_detail = {

                "password": request.data.get('password', None),
                "confirm_password": request.data.get("confirm_password", None)
            }
            context = super().get_serializer_context()
            context.update({"user_token_detail": user_token_detail,
                           "password_detail": password_detail})
            user_data_serializer = Reset_Password_Serializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():

                return Response(user_data_serializer.data['data'], status=status.HTTP_200_OK)
            else:
                return Response(user_data_serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" logged in """


@permission_classes((IsAuthenticated,))
class LoggedIn(Mixins, GeneralClass, ListAPIView):
    def get(self, request):
        logged_user = request.user
        user_obj_detail = UserDetail.objects.get(pk=logged_user.id)
        user_data = LoggedInUserSerializer(user_obj_detail)
        return Response(user_data.data)


""" Genrate OTP """


class GenerateOTP(ListAPIView):

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


class OTPVerification(ListAPIView):

    def post(self, request):
        try:
            user_obj = UserDetail.objects.filter(
                phone=request.data['phone']).first()

            if user_obj == None:
                context = {'error': "User with this phone number does not exist",
                           'isSuccess': "false", 'message': 'User with this phone number does not exist'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

            # datetime.datetime.strptime(str(_now),"%Y-%m-%d %H:%M:%S.%f")
            date_time = datetime.datetime.strptime(
                request.data['datetime'], "%Y-%m-%d %H:%M:%S.%f")

            if datetime.datetime.now() - date_time >= datetime.timedelta(seconds=140):
                context = {'error': "OTP expired",
                           'isSuccess': "false", 'message': 'OTP expired'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

            # hashed_otp_combo = pbkdf2_sha256.hash(str(request.data['entered_otp']) + str(date_time) + str(user_obj.id))
            pbkdf2_sha256.hash(
                str(request.data['entered_otp']) + str(date_time) + str(user_obj.user_obj))

            if pbkdf2_sha256.verify(str(request.data['entered_otp']) + str(date_time) + str(user_obj.user_obj), "$pbkdf2-sha256" + request.data['otp']):
                activation_key = urlsafe_base64_encode(force_bytes(user_obj.user_obj.pk)).decode(
                    'utf8') + '-' + default_token_generator.make_token(user_obj.user_obj)
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
        except Exception as error:
            context = {'error': str(error), 'isSuccess': "false",
                       'message': 'Unable to validate OTP'}
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Add User """


class AddUser(ListCreateAPIView):

    def post(self, request):
        try:
            address_detail = {
                "address": request.data.get('address', None),
                "city": request.data.get('city', None),
                "state": request.data.get('state', None),
                "country": request.data.get('country', None),
                "pincode": request.data.get('pincode', None),

            }
            address_created = False
            address_serializer = AddressSerializer(
                data=dict(address_detail))
            if address_serializer.is_valid():
                address_serializer.save()
                address_created = True
            else:
                raise ValidationError(address_serializer.errors)

            """ Auth user Data """

            user_data = {
                "first_name": request.data.get('first_name', None),
                "last_name": request.data.get('last_name', None),
                "email": request.data.get('email', None)

            }

            user_details_data = {
                "user_obj": 1,
                "phone": request.data.get('phone', None),
                "joining_date": request.data.get('joining_date', None),
                "role": request.data.get('role', None),
                "address": address_serializer.data['id'],
            }
            reporting_to = {
                "user_detail": 1,
                "user_role": request.data.get('role', None)[0],
                "reporting_to": request.data.get('reporting', None),
                "is_active": "true",
                "school": request.data.get('school', None)
            }

            print("reporting_to----------->", reporting_to)

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update({"user_data": user_data, "reporting_to": reporting_to,
                            "user_details_data": user_details_data})
            try:

                user_detail_serializer = AddUserSerializer(
                    data=dict(user_data), context=context)

                if user_detail_serializer.is_valid():
                    user_detail_serializer.save()
                    print("user_detail_serializer.data-",
                          user_detail_serializer.data)
                    context = {"message": "User is created successfully.", "isSuccess": True,
                               "data": user_detail_serializer.data, "statusCode": status.HTTP_200_OK}
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context = {"message": user_detail_serializer.errors, "isSuccess": False, "data": [],
                               "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}

                    return Response(context, status=status.status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as ex:
                print("TRACEback", traceback.print_exc())
                print("ERROR-------------", ex)
                logger.debug(ex)
                context = {
                    "message": ex, "isSuccess": False, "data": [], "statusCode": status.HTTP_200_OK}

                return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:

            if address_created == True:
                address_id = address_serializer.data['id']
                address_obj = Address.objects.get(pk=address_id)
                address_obj.delete()
            logger.debug(ex)
            context = {
                "message": ex, "isSuccess": False, "data": [], "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Update User """


class UpdateUser(ListCreateAPIView):

    def put(self, request, pk):
        try:

            address_detail = {
                "address": request.data.get('address', None),
                "city": request.data.get('city', None),
                "state": request.data.get('state', None),
                "country": request.data.get('country', None),
                "pincode": request.data.get('pincode', None),

            }
            address_qs = Address.objects.get(
                id=request.data.get('address_id', None))
            address_qs_serializer = AddressSerializer(
                address_qs, data=dict(address_detail), partial=True)
            if address_qs_serializer.is_valid():
                address_qs_serializer.save()

            else:
                raise ValidationError(address_qs.errors)
            user_data = {
                "first_name": request.data.get('first_name', None),
                "last_name": request.data.get('last_name', None),
                "email": request.data.get('email', None)
            }

            user_details_data = {
                "phone": request.data.get('phone', None),
                "joining_date": request.data.get('joining_date', None),
                "role": request.data.get('role', None),
                "address": request.data.get('address_id', None)

            }
            user_qs = User.objects.get(id=pk)

            user_qs_serializer = UpdateUserSerializer(
                user_qs, data=dict(user_data), partial=True)
            if user_qs_serializer.is_valid():
                user_qs_serializer.save()
                print("SAVE")
            else:
                print("user_qs_serializer.errors", user_qs_serializer.errors)
                return Response(user_qs_serializer.errors)

            user_details_qs = UserDetail.objects.filter(user_obj=pk)[0]

            user_detail_qs_serializer = UserDetailSerializer(
                user_details_qs, data=dict(user_details_data), partial=True)
            if user_detail_qs_serializer.is_valid():
                user_detail_qs_serializer.save()
            else:
                return Response(user_detail_qs_serializer.errors)
            role = request.data.get('role', None)
            user_role_id = Role.objects.filter(id=role[0])[0]
            print("user_role_id---", user_role_id)

            user_role_qs = UserRole.objects.filter(
                user=pk, role=request.data.get('previous_user_role', None))

            for user_role_obj in user_role_qs:

                user_role_obj.role = user_role_id
                user_role_obj.save()

            print("Role saved")
            user_detail_qs = UserDetail.objects.get(
                user_obj=request.data.get('reporting', None))

            print("user_detail_qs-------->", user_detail_qs)
            reporting_to_qs = ReportingTo.objects.filter(user_detail=pk, user_role=request.data.get(
                'previous_user_role', None), reporting_to=request.data.get('previous_reporting_to', None))
            print("#$$$$")
            for reporting_to_obj in reporting_to_qs:

                reporting_to_obj.user_role = user_role_id
                reporting_to_obj.reporting_to = user_detail_qs
                reporting_to_obj.save()
            print("reporting to Save")
            user_obj_data = {
                "id": user_qs.id
            }
            # return Response("User Updated", status=status.HTTP_200_OK)
            context = {"message": "User Updated successfully.", "isSuccess": True,
                       "data": user_obj_data, "statusCode": status.HTTP_200_OK}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERROR------", ex)
            print("traceback", traceback.print_exc())
            context = {
                "message": ex, "isSuccess": False, "data": [], "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserActivateDeactivate(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    def patch(self, request, pk):
        try:

            user_data = {

                "is_active": request.data.get('is_active', None),

            }

            user_details_data = {
                "reason_for_discontinution": request.data.get('reason_for_discontinution', None)
            }
            user_qs = User.objects.get(id=pk)

            user_qs_serializer = UpdateUserSerializer(
                user_qs, data=dict(user_data), partial=True)
            if user_qs_serializer.is_valid():
                user_qs_serializer.save()
                print("SAVE")
                user_details_qs = UserDetail.objects.filter(user_obj=pk)[0]

                user_detail_qs_serializer = UserDetailSerializer(
                    user_details_qs, data=dict(user_details_data), partial=True)
                if user_detail_qs_serializer.is_valid():
                    user_detail_qs_serializer.save()
                else:
                    print(user_detail_qs_serializer.errors)

                return Response("User Updated successfully", status=status.HTTP_200_OK)
            else:
                print("user_qs_serializer.errors", user_qs_serializer.errors)
                return Response(user_qs_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print("ERROR------", ex)
            print("traceback", traceback.print_exc())
            context = {
                "message": ex, "isSuccess": False, "data": [], "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Add role from user detail """


class AddRoleOfUserListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = ReportingTo

    def get_serializer_class(self):
        return ReportingToListSerializer

    def post(self, request):
        try:
            # print(request.data)
            role_detail = {
                "user": request.data.get('user_detail', None),
                "role": request.data.get('user_role', None),
                "school": ""
            }
            context = super().get_serializer_context()
            context.update({"role_detail": role_detail})
            user_role_serializer = ReportingToCreateSerializer(
                data=request.data, context=context)
            if user_role_serializer.is_valid():
                user_role_serializer.save()
                print("Serializer---", user_role_serializer.data)
                return Response(user_role_serializer.data, status=status.HTTP_200_OK)
            else:
                print(user_role_serializer.errors)
                return Response(user_role_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""  Reprting to list by User Detail """


class ReportingToListByUserDetailList(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    def get(self, request, pk):
        try:
            reporting_to_qs = ReportingTo.objects.filter(user_detail=pk)
            reporting_to_serializer = ReportingToListSerializer(
                reporting_to_qs, many=True)
            return Response(reporting_to_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            request_data = request.data.copy()
            user_detail = UserDetail.objects.filter(
                user_obj=request_data['user_detail'], role=request_data['previous_user_role'])[0]
            print(user_detail.role.all())
            user_detail.role.remove(request_data['previous_user_role'])
            user_detail.save()
            print(user_detail.role.all())
            user_detail.role.add(request_data['user_role'])
            user_detail.save()
            print(user_detail.role.all())
            user_role = Role.objects.filter(id=request_data['user_role'])[0]
            user_role_qs = UserRole.objects.filter(
                user=request_data['user_detail'], role=request_data['previous_user_role'])[0]
            user_role_qs.role = user_role
            user_role_qs.save()

            user_detail_qs = UserDetail.objects.filter(
                user_obj=request_data['reporting_to'])[0]
            reporting_to_qs = ReportingTo.objects.filter(
                user_detail=request_data['user_detail'], user_role=request_data['previous_user_role'])[0]
            reporting_to_qs.reporting_to = user_detail_qs
            reporting_to_qs.user_role = user_role
            reporting_to_qs.save()

            return Response("Updated Successfully", status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERROR--------", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" School list according to User """


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


""" User Role Update and Retrive """


class UserRoleRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = UserRole
    filterset_class = UserRoleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserRoleListSerializer
        if self.request.method == 'PUT':
            return UserRoleSerializer
        if self.request.method == 'PATCH':
            return UserRoleSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


"""  Get UsersBasedOnSchoolID """


class UserListBySchoolID(GeneralClass, Mixins, ListCreateAPIView):
    model = UserRole
    serializer_class = SchoolUserRoleSerializers
    filterset_class = UserRoleFilter

    # filter_backends = (filters.DjangoFilterBackend,)

    def get(self, request, pk):
        try:

            user_role_list = UserRole.objects.filter(school=pk)
            print(user_role_list)
            filtered_data = UserRoleFilter(
                request.GET, queryset=user_role_list)
            filtered_quersyet = filtered_data.qs
            user_role_list = filtered_quersyet.all()

            page = self.paginate_queryset(user_role_list)
            if page is not None:
                serializer = self.get_serializer(
                    page, many=True)
                return self.get_paginated_response(serializer.data)
            user_role_serializer = SchoolUserRoleSerializers(
                user_role_list, many=True)
            return Response(user_role_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" S3 Key Access """


class KeyAccessOfS3(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request):
        try:
            crediential = {}
            crediential['aws_bucket_name'] = genrate_encrypted_string(
                os.environ.get('AWS_STORAGE_BUCKET_NAME'))
            crediential['aws_region_name'] = genrate_encrypted_string(
                os.environ.get('AWS_S3_REGION_NAME'))
            crediential['aws_secret_access_key'] = genrate_encrypted_string(
                os.environ.get('AWS_SECRET_ACCESS_KEY'))
            crediential['aws_access_key_id'] = genrate_encrypted_string(
                os.environ.get('AWS_ACCESS_KEY_ID'))

            decrypt_value = genrate_decrypted_string(
                crediential['aws_bucket_name'])
            print("###############", decrypt_value)
            return Response(crediential, status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERROR", ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" **********    Bulk Upload """


class AddAccount(ListCreateAPIView):

    def post(self, request):
        try:
            print("AddAccount Called")
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_user = []
            for i, f in enumerate(df, start=1):
                f['role'] = ast.literal_eval(f['role'])
                if not math.isnan(f['id']) and f['isDeleted'] == False:
                    auth_user = User.objects.filter(user_obj=id)[0]
                    auth_user.first_name = f.get('first_name', None)
                    auth_user.last_name = f.get('last_name', None)
                    auth_user.email = f.get('email', None)
                    auth_user.save()
                    user_detail_qs = UserDetail.objects.filter(user_obj=id)[0]
                    user_detail_qs.phone = f.get('phone', None)
                    user_detail_qs.joining_date = f.get('joining_date', None)
                    user_detail_qs.save()
                    address_qs = Address.objects.filter(
                        id=user_detail_qs.address)[0]
                    address_qs.address = f.get('address', None)
                    address_qs.city = f.get('city', None)
                    address_qs.state = f.get('state', None)
                    address_qs.country = f.get('country', None)
                    address_qs.address = f.get('address', None)
                    address_qs.save()

                    added_user.append(
                        {
                            "id": user_detail_qs.user_obj,
                            "email": auth_user.first_name,
                            "first_name": auth_user.first_name,
                            "last_name": auth_user.last_name,
                            "phone": user_detail_qs.phone,
                            "address": address_qs.id
                        }
                    )

                elif not math.isnan(f['id']) and f['isDeleted'] == True:
                    print("Deletion", f)
                    auth_user = User.objects.filter(user_obj=id)[0]
                    user_detail_qs = UserDetail.objects.filter(user_obj=id)[0]
                    address_qs = Address.objects.filter(
                        id=user_detail_qs.address)[0]
                    address_qs.delete()
                    user_detail_qs.delete()
                    added_user.append(
                        {
                            "id": user_detail_qs.user_obj,
                            "email": auth_user.first_name,
                            "first_name": auth_user.first_name,
                            "last_name": auth_user.last_name,
                            "phone": user_detail_qs.phone,
                            "address": address_qs.id
                        }
                    )

                else:
                    print("Creation", f)
                    address_detail = {
                        "address": f.get('address', None),
                        "city": f.get('city', None),
                        "state": f.get('state', None),
                        "country": f.get('country', None),
                        "pincode": f.get('pin', None),

                    }
                    address_serializer = AddressSerializer(
                        data=dict(address_detail))
                    if address_serializer.is_valid():
                        address_serializer.save()
                        print(address_serializer.data)
                    else:
                        print("address_serializer._errors",
                              address_serializer._errors)
                        raise ValidationError(address_serializer.errors)

                        """ Auth user Data """

                    user_data = {
                        "first_name": f.get('first_name', None),
                        "last_name": f.get('last_name', None),
                        "email": f.get('email', None)

                    }

                    user_details_data = {
                        "user_obj": 1,
                        "phone": f.get('phone', None),
                        "joining_date": f.get('joining_date', None),
                        "address": address_serializer.data['id'],
                        "role": f.get('role', None)
                    }

                    """  Pass dictionary through Context """
                    context = super().get_serializer_context()
                    context.update({"user_data": user_data,
                                    "user_details_data": user_details_data})
                    try:
                        user_detail_serializer = AddUserSerializer(
                            data=dict(user_data), context=context)

                        if user_detail_serializer.is_valid():
                            user_detail_serializer.save()
                            added_user.append(
                                {
                                    "id": user_detail_serializer.data['user_detail_data']['user_obj'],
                                    "email": user_detail_serializer.data['email'],
                                    "first_name": user_detail_serializer.data['first_name'],
                                    "last_name": user_detail_serializer.data['last_name'],
                                    "phone": user_detail_serializer.data['user_detail_data']['phone'],
                                    "address": user_detail_serializer.data['user_detail_data']['address']
                                }
                            )
                        else:
                            print(user_detail_serializer.errors)

                    except Exception as ex:
                        print("error", ex)
                        print("traceback", traceback.print_exc())
                        logger.debug(ex)
                        context = {"isSuccess": False, "message": "Issue Account",
                                   "error": ex, "data": ""}
                        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            keys = added_user[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_user)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            context = {"isSuccess": True, "message": "Account Added sucessfully",
                       "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            context = {"isSuccess": False, "message": "Issue User",
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddSchool(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            print(df)
            added_school = []
            for i, f in enumerate(df, start=1):
                print(f['licence_start'])
                # licence_start = datetime.datetime.strptime(str(f.get('licence_start', None)), '%d/%m/%Y').date()
                licence_start = f.get('licence_start', None)

                # print(licence_start)
                # licence_start = f.get('licence_start', None)
                # licence_start = licence_start.strftime('%Y-%m-%d')
                # print(licence_start)
                if not math.isnan(f['id']) and f['is_Deleted'] == False:
                    school_qs = School.objects.filter(id=f['id'])[0]
                    address_qs = Address.objects.filter(
                        id=school_qs['address'])[0]
                    address_qs.address = f.get('address', None)
                    address_qs.city = f.get('city', None)
                    address_qs.state = f.get('state', None)
                    address_qs.country = f.get('country', None)
                    address_qs.save()
                    license_qs = License.objects.filter(
                        id=school_qs['license'])[0]
                    license_qs.total_no_of_user = f.get('no._of_users', None)
                    license_qs.total_no_of_children = f.get(
                        'no_of_children', None)
                    license_qs.licence_from = licence_start
                    license_qs.licence_till = add_months(
                        f.get('licence_start', None), f.get('no_of_month', None))
                    license_qs.save()
                    school_qs.name = f.get('name', None)
                    school_qs.type = f.get('type', None)
                    school_qs.logo = f.get('logo', None)
                    school_qs.save()

                    package_data = f.get('package', None)
                    print(package_data)
                    for i, da in enumerate(json.loads(package_data), start=1):
                        schoolPackage_qs = SchoolPackage.objects.filter(
                            school=school_qs['id'])[0]
                        schoolPackage_qs.package = da['pakage']
                        schoolPackage_qs.custom_materials = da['customized_material']
                        schoolPackage_qs.save()

                    schoolCalender_qs = SchoolCalender.objects.filter(
                        school=school_qs['id'])
                    schoolCalender_qs.session_till = addYears(
                        schoolCalender_qs.session_from, f.get('school_calender_for_no_of_year', None))
                    schoolCalender_qs.save()
                    added_school.append(
                        {
                            "address": school_qs.data['address'],
                            "license": school_qs.data['license'],
                            "school": school_qs.data['id']
                        }
                    )
                elif not math.isnan(f['id']) and f['is_Deleted'] == True:
                    school_qs = School.objects.filter(id=f['id']).delete()
                    SchoolCalender.objects.filter(
                        school=school_qs['id']).delete()
                    UserRole.objects.filter(school=school_qs['id']).delete()
                    SchoolPackage.objects.filter(
                        school=school_qs['id']).delete()
                    added_school.append(
                        {
                            "address": school_qs.data['address'],
                            "license": school_qs.data['license'],
                            "school": school_qs.data['id']
                        }
                    )

                else:
                    print("CREATING")
                    address_detail = {
                        "address": f.get('address', None),
                        "city": f.get('city', None),
                        "state": f.get('state', None),
                        "country": f.get('country', None),
                    }

                    address_serializer = AddressSerializer(
                        data=dict(address_detail))
                    if address_serializer.is_valid():
                        address_serializer.save()
                        print(address_serializer.data)
                    else:
                        print("address_serializer._errors",
                              address_serializer._errors)
                        raise ValidationError(address_serializer.errors)

                    licence_detail = {
                        "total_no_of_user": f.get('no._of_users', None),
                        "total_no_of_children": f.get('no_of_children', None),
                        "licence_from": licence_start,
                        "licence_till": add_months(f.get('licence_start', None), f.get('no_of_month', None)),
                        "created_by": f.get('created_by', None),
                    }

                    licenseCreateSerializer = LicenseCreateSerializer(
                        data=dict(licence_detail))

                    if licenseCreateSerializer.is_valid():
                        licenseCreateSerializer.save()
                    else:
                        raise ValidationError(licenseCreateSerializer.errors)

                    school_detail = {
                        "name": f.get('name', None),
                        "type": f.get('type', None),
                        "logo": f.get('logo', None),
                        "address": address_serializer.data['id'],
                        "license": licenseCreateSerializer.data['id'],
                    }

                    schoolCreateSerializer = SchoolCreateSerializer(
                        data=dict(school_detail))
                    if schoolCreateSerializer.is_valid():
                        schoolCreateSerializer.save()
                    else:
                        raise ValidationError(schoolCreateSerializer.errors)

                    package_data = f.get('package', None)
                    print(package_data)
                    for i, da in enumerate(json.loads(package_data), start=1):
                        print("da", da)
                        school_package_detail = {
                            "school": schoolCreateSerializer.data['id'],
                            "package": da['pakage'],
                            # "from_date": f.get('from_date', None),
                            # "to_date": f.get('to_date', None),
                            "custom_materials": da['customized_material'],
                        }

                        schoolPackageCreateSerializer = SchoolPackageCreateSerializer(
                            data=dict(school_package_detail))
                        if schoolPackageCreateSerializer.is_valid():
                            schoolPackageCreateSerializer.save()
                        else:
                            raise ValidationError(
                                schoolPackageCreateSerializer.errors)

                    school_calender_detail = {
                        "school": schoolCreateSerializer.data['id'],
                        "session_from": date.today(),
                        "session_till": addYears(date.today(), f.get('school_calender_for_no_of_year', None)),
                    }

                    schoolCalendarCreateSerializer = SchoolCalendarCreateSerializer(
                        data=dict(school_calender_detail))

                    if schoolCalendarCreateSerializer.is_valid():
                        schoolCalendarCreateSerializer.save()
                    else:
                        raise ValidationError(
                            schoolCalendarCreateSerializer.errors)
                    user_role_detail = {
                        "user": f.get('account_id', None),
                        "role": Role.objects.filter(name="School Account Owner")[0].id,
                        "school": schoolCreateSerializer.data['id']
                    }

                    userRoleSerializer = UserRoleSerializer(
                        data=dict(user_role_detail))
                    if userRoleSerializer.is_valid():
                        userRoleSerializer.save()
                    else:
                        raise ValidationError(userRoleSerializer.errors)

                    added_school.append(
                        {
                            "address": address_serializer.data['id'],
                            "license": licenseCreateSerializer.data['id'],
                            "school": schoolCreateSerializer.data['id']


                        }
                    )

            keys = added_school[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_school)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "School Added sucessfully",
                       "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            # return Response(ex)
            context = {"isSuccess": False, "message": "Issue School",
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddSchoolGradeSubject(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_school_grade_subject = []

            for i, f in enumerate(df, start=1):
                # f['subject'] = json.loads(f['subject'])
                f['subject'] = ast.literal_eval(f['subject'])
                if not math.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    schoolGradeSubject_qs = SchoolGradeSubject.objects.filter(id=f['id'])[
                        0]
                    schoolGradeSubject_qs.school = f['school']
                    schoolGradeSubject_qs.grade = f['grade']
                    schoolGradeSubject_qs.subject = json.loads(f['subject'])
                    schoolGradeSubject_qs.save()
                    added_school_grade_subject.append(schoolGradeSubject_qs)
                elif not math.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    schoolGradeSubject_qs = SchoolGradeSubject.objects.filter(id=f['id'])[
                        0]
                    added_school_grade_subject.append(schoolGradeSubject_qs)
                    schoolGradeSubject_qs.delete()
                else:
                    print("Create")
                    # f['subject'] = json.loads(f['subject'])
                    schoolGradeSubject_serializer = SchoolGradeSubjectCreateSerializer(
                        data=dict(f))
                    if schoolGradeSubject_serializer.is_valid():
                        schoolGradeSubject_serializer.save()
                        added_school_grade_subject.append(
                            schoolGradeSubject_serializer.data)
                        print(schoolGradeSubject_serializer.data)
                    else:
                        print("schoolGradeSubject_serializer._errors",
                              schoolGradeSubject_serializer._errors)
                        raise ValidationError(
                            schoolGradeSubject_serializer.errors)

            keys = added_school_grade_subject[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_school_grade_subject)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "School Grade Subject Added sucessfully",
                       "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            # return Response(ex)
            context = {"isSuccess": False, "message": "Issue School subject grade",
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Upload USERS """


class AddUserData(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_user = []

            for i, f in enumerate(df, start=1):
                f['role'] = ast.literal_eval(f['role'])
                if not m.isnan(f['id']) and f['is_Deleted'] == False:
                    print("UPDATION")
                    auth_user = User.objects.filter(user_obj=id)[0]
                    auth_user.first_name = f.get('first_name', None)
                    auth_user.last_name = f.get('last_name', None)
                    auth_user.email = f.get('email', None)
                    auth_user.save()
                    user_detail_qs = UserDetail.objects.filter(user_obj=id)[0]
                    user_detail_qs.phone = f.get('phone', None)
                    user_detail_qs.joining_date = f.get('joining_date', None)
                    user_detail_qs.save()
                    address_qs = Address.objects.filter(
                        id=user_detail_qs.address)[0]
                    address_qs.address = f.get('address', None)
                    address_qs.city = f.get('city', None)
                    address_qs.state = f.get('state', None)
                    address_qs.country = f.get('country', None)
                    address_qs.address = f.get('address', None)
                    address_qs.save()

                    role = f.get('role', None)
                    print(role)
                    for i, da in enumerate(json.loads(role), start=1):
                        user_role_qs = UserRole.objects.filter(user=id)[0]
                        user_role_qs.user = da['user']
                        user_role_qs.role = da['role']
                        user_role_qs.school = da['school']
                        user_role_qs.save()

                        reporting_to_qs = ReportingTo.objects.filter(
                            user_detail=id)
                        reporting_to_qs.user_detail = id
                        reporting_to_qs.user_role = da['role']
                        reporting_to_qs.reporting_to = f.get(
                            'reporting_to', None)
                        reporting_to_qs.save()

                    added_user.append(
                        {
                            "id": user_detail_qs.user_obj,
                            "email": auth_user.first_name,
                            "first_name": auth_user.first_name,
                            "last_name": auth_user.last_name,
                            "phone": user_detail_qs.phone,
                            "address": address_qs.id,
                            "school": f.get('school', None)
                        }
                    )
                elif not m.isnan(f['id']) and f['is_Deleted'] == True:
                    print("Deletion", f)
                    auth_user = User.objects.filter(user_obj=id)[0]
                    user_detail_qs = UserDetail.objects.filter(user_obj=id)[0]
                    address_qs = Address.objects.filter(
                        id=user_detail_qs.address)[0]
                    user_role_qs = UserRole.objects.filter(user=id)[0]
                    user_reporting_qs = ReportingTo.objects.filter(user_detail=id)[
                        0]
                    user_reporting_qs.delete()
                    user_role_qs.delete()
                    address_qs.delete()
                    user_detail_qs.delete()
                    added_user.append(
                        {
                            "id": user_detail_qs.user_obj,
                            "email": auth_user.first_name,
                            "first_name": auth_user.first_name,
                            "last_name": auth_user.last_name,
                            "phone": user_detail_qs.phone,
                            "address": address_qs.id,
                            "school": f.get('school', None)
                        }
                    )

                else:
                    print("Create")

                    address_detail = {
                        "address": f.get('address', None),
                        "city": f.get('city', None),
                        "state": f.get('state', None),
                        "country": f.get('country', None),
                        "pincode": f.get('pin', None),

                    }
                    address_serializer = AddressSerializer(
                        data=dict(address_detail))
                    if address_serializer.is_valid():
                        address_serializer.save()
                        print(address_serializer.data)
                    else:
                        print("address_serializer._errors",
                              address_serializer._errors)
                        raise ValidationError(address_serializer.errors)

                        """ Auth user Data """

                    user_data = {
                        "first_name": f.get('first_name', None),
                        "last_name": f.get('last_name', None),
                        "email": f.get('email', None)

                    }

                    user_details_data = {
                        "user_obj": 1,
                        "phone": f.get('phone', None),
                        "role": f.get('role', None),
                        "address": address_serializer.data['id'],
                    }

                    """  Pass dictionary through Context """
                    context = super().get_serializer_context()
                    context.update({"user_data": user_data,
                                    "user_details_data": user_details_data})
                    try:
                        user_detail_serializer = AddUserSerializer(
                            data=dict(user_data), context=context)

                        if user_detail_serializer.is_valid():
                            user_detail_serializer.save()
                            added_user.append(
                                {
                                    "id": user_detail_serializer.data['user_detail_data']['user_obj'],
                                    "email": user_detail_serializer.data['email'],
                                    "first_name": user_detail_serializer.data['first_name'],
                                    "last_name": user_detail_serializer.data['last_name'],
                                    "phone": user_detail_serializer.data['user_detail_data']['phone'],
                                    "address": user_detail_serializer.data['user_detail_data']['address'],
                                    "school": f.get('school', None)
                                }
                            )
                        else:
                            print(user_detail_serializer.errors)
                    except Exception as ex:
                        print("error", ex)
                        print("traceback", traceback.print_exc())
                        logger.debug(ex)
                        return Response(ex)
                    """ Creation of UserRole"""
                    try:
                        role_data = f.get('role', None)
                        print(role_data)
                        role_detail = {
                            "user": user_detail_serializer.data['user_detail_data']['user_obj'],
                            "role": role_data[0],
                            "school": f.get('school', None)
                        }
                        userRoleSerializer = UserRoleSerializer(
                            data=dict(role_detail))
                        if userRoleSerializer.is_valid():
                            userRoleSerializer.save()
                        else:
                            raise ValidationError(userRoleSerializer.errors)

                    except Exception as ex:
                        print("error", ex)
                        print("traceback", traceback.print_exc())
                        logger.debug(ex)
                        return Response(ex)

                    """ Creation of Reporting to """

                    try:
                        user_reporting_data = {
                            "user_detail": user_detail_serializer.data['user_detail_data']['user_obj'],
                            "user_role": f['role'][0],
                            "reporting_to": f['reporting_to']
                        }

                        reporting_to_serializer = ReportingToSerializer(
                            data=dict(user_reporting_data))
                        if reporting_to_serializer.is_valid():
                            reporting_to_serializer.save()
                        else:
                            raise ValidationError(
                                reporting_to_serializer.errors)
                    except Exception as ex:
                        print("error", ex)
                        print("traceback", traceback.print_exc())
                        logger.debug(ex)
                        return Response(ex)

            keys = added_user[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_user)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "User Added sucessfully",
                       "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            print(traceback.format_exc())
            logger.debug(ex)
            # return Response(ex)
            context = {"isSuccess": False, "message": "Issue User",
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class SchoolAccountListCreate(GeneralClass,Mixins,ListCreateAPIView):
#     model = User
#     serializer_class = AddUserSerializer


#     def post(self,request):
#         try:
#             user_details_data = {
#                 'first_name':request.data.get('first_name',None),
#                 'last_name':request.data.get('last_name',None),

#             }

#         except Exception as ex:
#             return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Get role by loggin id """


@permission_classes((IsAuthenticated,))
class getRolesByLoggedinUserId(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request):
        try:
            logged_user = request.user
            user_obj = UserDetail.objects.filter(user_obj=logged_user.id)[0]
            for role in user_obj.role.all():

                role_name = Role.objects.filter(name=role)[0]
                if role_name.name == "School Account Owner":
                    role_obj = Role.objects.filter(name="School Admin")
                    role_obj_serilaizer = RoleListSerializer(
                        role_obj, many=True)
                    return Response(role_obj_serilaizer.data, status=status.HTTP_200_OK)
                elif role_name.name == "School Admin":
                    role_obj = Role.objects.filter(
                        name__in=["School Admin", "School Associate", "Teacher"])
                    role_obj_serilaizer = RoleListSerializer(
                        role_obj, many=True)
                    return Response(role_obj_serilaizer.data, status=status.HTTP_200_OK)
                elif role_name.name == "School Associate":
                    role_obj = Role.objects.filter(
                        name__in=["School Admin", "School Associate", "Teacher"])
                    role_obj_serilaizer = RoleListSerializer(
                        role_obj, many=True)
                    return Response(role_obj_serilaizer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Role Not Found", status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("ERROR-----", ex)
            print("TRACEBACK---------", traceback.print_exc())
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""get reportings to based on selected role """


class GetReportingToBasedOnSelectedRole(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            print("request")
            role_name = Role.objects.filter(id=request.data.get(
                'role', None))[0]
            print("role_name.name", role_name.name)
            if role_name.name == "School Admin":
                role_obj = Role.objects.filter(name="School Account Owner")[0]

                user_role_qs = UserRole.objects.filter(
                    role=role_obj, school=request.data.get('school', None))
                if user_role_qs:
                    user_role_qs_serializer = ReportingToRoleSerializer(
                        user_role_qs, many=True)
                    return Response(user_role_qs_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Reporting to Not Found", status=status.HTTP_404_NOT_FOUND)
            elif role_name.name == "School Associate":
                role_obj = Role.objects.filter(
                    name__in=["School Admin", "School Account Owner"])[0]

                user_role_qs = UserRole.objects.filter(
                    role=role_obj, school=request.data.get('school', None))
                if user_role_qs:
                    user_role_qs_serializer = ReportingToRoleSerializer(
                        user_role_qs, many=True)
                    return Response(user_role_qs_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Reporting to Not Found", status=status.HTTP_404_NOT_FOUND)
            elif role_name.name == "Teacher":
                role_obj = Role.objects.filter(
                    name__in=["School Admin", "School Account Owner", "School Associate"])[0]

                user_role_qs = UserRole.objects.filter(
                    role=role_obj, school=request.data.get('school', None))
                if user_role_qs:
                    user_role_qs_serializer = ReportingToRoleSerializer(
                        user_role_qs, many=True)
                    return Response(user_role_qs_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Reporting to Not Found", status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("ERROR-----", ex)
            print("TRACEBACK---------", traceback.print_exc())
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
