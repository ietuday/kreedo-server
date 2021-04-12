"""
    DJANGO LIBRARY IMPORT
"""
from .serializer import*
from ..models import*
from .filters import*
from kreedo.general_views import Mixins, GeneralClass
from kreedo.conf.logger_test import*
from kreedo.conf.logger import CustomFormatter
import traceback
import logging
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from django.shortcuts import render
"""
    REST LIBRARY IMPORT
"""
"""
    IMPORT CORE FILES 
"""
"""
    IMPORT USER APP FILE
"""

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
    serializer_class = RoleSerializer
    filterset_class = RoleFilter


""" Role Retrive, Update and Delete  API"""


class RoleRetriveUpdateDestroy(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
    model = Role
    serializer_class = RoleSerializer
    filterset_class = RoleFilter


""" User Type List and Create """


class UserTypeListCreate(Mixins, GeneralClass, ListCreateAPIView):
    model = UserType
    serializer_class = UserTypeSerializer
    filterset_class = UserTypeFilter


""" Retrive ,Update and Delete User Type """


class UserTypeRetriveUpdateDestroy(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
    model = UserType
    serializer_class = UserTypeSerializer
    filterset_class = UserTypeFilter


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


""" User Register API """


class UserRegister(CreateAPIView):
    def post(self, request):
        try:

            address_detail = {
                "country": request.data.get('country', None),
                "state": request.data.get('state', None),
                "city": request.data.get('city', None),
                "address": request.data.get('address', None),
                "pincode": request.data.get('pincode', None)
            }

            address_serializer = AddressSerializer(data=address_detail)
            if address_serializer.is_valid():
                address_serializer.save()

            else:
                print("address_serializer._errors", address_serializer._errors)

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
                user_data_serializer = UserRegisterSerializer(
                data=dict(user_data), context=context)
            except Exception as ex:
                context = {"error":ex, "statusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)
            if user_data_serializer.is_valid():
                user_data_serializer.save()
                context = {"message": "User is created successfully. User will get reset password email within 24 hours.",
                           "data": user_data_serializer.data, "statusCode": status.HTTP_200_OK}

                return Response(context)
            else:
                # logger.debug("user_data_serializer.errors",
                #       user_data_serializer.errors)
                context = {"error":user_data_serializer.errors,"statusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)

        except Exception as ex:
            # logger.debug("Entering Register method",ex)
            context={"error":ex, "statusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" Email Confirm Verification"""


class EmailConfirmVerify(CreateAPIView):
    # model = User
    serializer_class = UserEmailVerifySerializer

    def get(self, request, uidb64, token):
        try:
            print("Email Confirm---->", uidb64, token)
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
                print("error",ex)
                context={"error":ex, "StatusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)    
            
            if user_serializar.is_valid():
                print("user_serializar----------->", user_serializar)
                context = {"mail_t": user_serializar.data,"message": 'Email Verified',
                        "statusCode":status.HTTP_200_OK}
                return Response(context)
            else:
                print("error-------------->", user_serializar.errors)
                context={"error":user_serializar.errors, "StatusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)

        except Exception as ex:
            print("exception", ex)
            print("Traceback", traceback.print_exc())
            context={"error":ex, "StatusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" Login """


class UserLogin(CreateAPIView):

    def post(self, request):
        try:

            user_data_serializer = UserLoginSerializer(data=request.data)
            if user_data_serializer.is_valid():
                context = {"data": user_data_serializer.data}
                return Response(context)
            else:
                context = {"error": user_data_serializer.errors,
                           }
                return Response(context)
        except Exception as ex:

            context = {"error": ex}
            return Response(context)


""" Forget password """


class ForgetPassword(CreateAPIView):
    # model = User

    def post(self, request):
        try:

            user_data_serializer = UserForgetSerializer(data=request.data)

            if user_data_serializer.is_valid():
                print("User Serializer", user_data_serializer)
                context = {"message": "Token send to user",
                "statusCode":status.HTTP_200_OK}
                return Response(context)
            else:
                context = {"error":user_data_serializer.errors, "statusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)
        except Exception as ex:
            context = {"error":ex, "statusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


"""CHANGE PASSWORD """

# @permission_classes((IsAuthenticated,))
class ChangePassword(CreateAPIView):
    # model = User
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print("change_password",request.data)

            password_detail = {
                "username": request.user.username,
                "old_password": request.data.get('old_password', None),
                "new_password": request.data.get('new_password', None)
            }
            context = super().get_serializer_context()
            context.update({"password_detail": password_detail})
            print("password_detail",password_detail)
            user_data_serializer = UserChangePasswordSerializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():
                context = {"data": user_data_serializer.data,
                           "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:
                context = {"error": user_data_serializer.errors,"statusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)
        except Exception as ex:
            context = {"error": ex,"statusCode":status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" Rest Email Confirm """


class ResetPasswordConfirm(CreateAPIView):
    # model = User
    serializer_class = User_Password_Reseted_Mail_Serializer
    def get(self, request, uidb64, token):
        try:
            user_token_detail = {
                "uidb64": uidb64,
                "token": token
            }
            print("User Token detail")
            context = super().get_serializer_context()
            context.update({"user_token_detail": user_token_detail})
            user_data_serializer = User_Password_Reseted_Mail_Serializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():
                context = {"mail_t": user_data_serializer.data,
                           'message': 'Password has been reset.'}
                return Response(context)
            else:
                context = {"error": user_data_serializer.data}
                return Response(context)

        except Exception as ex:
            context = {"error": ex}
            return Response(context)
