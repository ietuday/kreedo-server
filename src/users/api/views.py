from kreedo.general_views import Mixins, GeneralClass
import logging
import traceback
from .filters import*
from ..models import*
from .serializer import*
from django.contrib.auth.models import User
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.shortcuts import render
from kreedo.conf.logger import CustomFormatter
from kreedo.conf.logger_test import*
from rest_framework.response import Response
"""
    REST LIBRARY IMPORT
"""

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

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

            user_data_serializer = UserRegisterSerializer(
                data=dict(user_data), context=context)
            if user_data_serializer.is_valid():
                user_data_serializer.save()
                context = {"message": "User is created successfully. User will get reset password email within 24 hours.",
                           "data": user_data_serializer.data}

                return Response(context)
            else:
                print("user_data_serializer.errors",
                      user_data_serializer.errors)
                context = {"user_error": user_data_serializer.errors}
                return Response(context)

        except Exception as ex:
            logger.debug("Entering Register method")
            context = {"error": ex}
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

            user_data_serializer = UserEmailVerifySerializer(
                data=request.data, context=context)

            if user_data_serializer.is_valid():
                user_data_serializer.save()
                print("user_data_serializer", user_data_serializer)
                context = {"mail_t": user_data_serializer.data,
                           'message': 'Email Verified'}
                return Response(context)
            else:
                print("error", user_data_serializer.data)
                context = {"error": user_data_serializer.data}
                return Response(context)

        except Exception as ex:
            print("exception", ex)
            print("Traceback", traceback.print_exc())
            context = {"error": ex}
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
                context = {"message": "Token send to user"}
                return Response(context)
            else:
                context = {"error": user_data_serializer.errors}
                return Response(context)
        except Exception as ex:
            context = {"error": ex}
            return Response(context)


"""CHANGE PASSWORD """


class ChangePassword(CreateAPIView):
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
                context = {"data": user_data_serializer.data,
                           "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:
                context = {"error": user_data_serializer.errors}
                return Response(context)
        except Exception as ex:
            context = {"error": e}
            return Response(context)


""" Rest Email Confirm """


class ResetPasswordConfirm(CreateAPIView):
    # model = User
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
