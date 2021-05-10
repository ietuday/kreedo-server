"""
    DJANGO LIBRARY IMPORT
"""
import math
import pdb
import csv
from pandas import DataFrame
import json
from .serializer import*
from ..models import*
from .filters import*
from kreedo.general_views import Mixins, GeneralClass
from kreedo.conf.logger import CustomFormatter
import traceback
import logging
import pandas as pd

from rest_framework .generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from django.core.exceptions import ValidationError
from django.shortcuts import render
from users.api.custum_storage import FileStorage
from schools.models import*
from schools.api.serializer import*

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


class UserTypeRetriveUpdateDelete(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
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
                context = {"message": "User is created successfully. User will get reset password email within 24 hours.",
                           "data": user_detail.data, "statusCode": status.HTTP_200_OK}

                return Response(context)
            else:
                logger.debug(
                    user_detail.errors)
                context = {"error": user_detail.errors,
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)

        except Exception as ex:
            if address_created == True:
                address_id = address_serializer.data['id']
                address_obj = Address.objects.get(pk=address_id)
                address_obj.delete()
            logger.debug(ex)
            context = {"error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" Email Confirm Verification"""


class EmailConfirmVerify(ListAPIView):
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
                print("error", ex)
                context = {"error": ex,
                           "StatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)

            if user_serializar.is_valid():
                print("user_serializar----------->", user_serializar)
                context = {"mail_t": user_serializar.data, "message": 'Email Verified',
                           "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:
                print("error-------------->", user_serializar.errors)
                context = {"error": user_serializar.errors,
                           "StatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)

        except Exception as ex:
            print("exception", ex)
            print("Traceback", traceback.print_exc())
            context = {"error": ex,
                       "StatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" Login """


class UserLogin(CreateAPIView):
    model = User

    def post(self, request):
        try:

            user_data_serializer = UserLoginSerializer(data=request.data)
            if user_data_serializer.is_valid():
                context = {'isSuccess': True, 'message': "Login Successfull",
                           'data': user_data_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:
                context = {'isSuccess': False, "error": user_data_serializer.errors,
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)
        except Exception as ex:
            context = {'isSuccess': False, 'message': "Something went wrong",
                       'error': ex, "statusCode": status.HTTP_400_BAD_REQUEST}
            return Response(context)


""" Forget password """


class ForgetPassword(CreateAPIView):
    # model = User

    def post(self, request):
        try:

            user_data_serializer = UserForgetSerializer(data=request.data)

            if user_data_serializer.is_valid():
                print("User Serializer", user_data_serializer)
                context = {"message": "Token send to user", 'isSuccess': True,
                           "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:
                context = {"error": user_data_serializer.errors, 'isSuccess': False,
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)
        except Exception as ex:

            context = {"error": ex, 'isSuccess': False,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


"""CHANGE PASSWORD """

# @permission_classes((IsAuthenticated,))


class ChangePassword(CreateAPIView):
    # model = User
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print("change_password", request.data)

            password_detail = {
                "username": request.user.username,
                "old_password": request.data.get('old_password', None),
                "new_password": request.data.get('new_password', None)
            }
            context = super().get_serializer_context()
            context.update({"password_detail": password_detail})
            print("password_detail", password_detail)
            user_data_serializer = UserChangePasswordSerializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():
                context = {"data": user_data_serializer.data,
                           "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:
                context = {"error": user_data_serializer.errors,
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)
        except Exception as ex:
            context = {"error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" Rest Email Confirm """


class ResetPasswordConfirm(CreateAPIView):
    # model = User
    serializer_class = User_Password_Reseted_Mail_Serializer

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
            user_data_serializer = User_Password_Reseted_Mail_Serializer(
                data=request.data, context=context)
            if user_data_serializer.is_valid():
                context = {'isSuccess': True,
                           'message': 'Password has been reset.',
                           "statusCode": status.HTTP_200_OK}
                return Response(context)
            else:
                context = {"error": user_data_serializer.data,
                           "statusCode": status.HTTP_404_NOT_FOUND, 'isSuccess': False}
                return Response(context)

        except Exception as ex:
            context = {"error": ex, 'isSuccess': False,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" logged in """


@permission_classes((IsAuthenticated,))
class LoggedIn(GeneralClass, ListAPIView):

    def get(self, request):
        logged_user = request.user
        user_obj_detail = UserDetail.objects.get(pk=logged_user.id)
        user_data = LoggedInUserSerializer(user_obj_detail)
        return Response(user_data.data)


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
                print("address_serializer._errors",
                      address_serializer._errors)
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
                "address": address_serializer.data['id'],
            }
            reporting_to = {
                "user_detail": 1,
                "user_role": request.data.get('role', None),
                "reporting_to": request.data.get('reporting_to', None),
                "is_active": "true"
            }

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update({"user_data": user_data, "reporting_to": reporting_to,
                            "user_details_data": user_details_data})
            try:

                user_detail_serializer = AddUserSerializer(
                    data=dict(user_data), context=context)

                if user_detail_serializer.is_valid():
                    user_detail_serializer.save()
                    context = {"message": "User is created successfully.",
                               "data": user_detail_serializer.data, "statusCode": status.HTTP_200_OK}
                    return Response(context)
                else:
                    context = {"error": user_detail_serializer.errors,
                               "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}

                    return Response(context)
            except Exception as ex:

                logger.debug(ex)
                context = {
                    "error": ex, "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}

                return Response(context)

        except Exception as ex:

            if address_created == True:
                address_id = address_serializer.data['id']
                address_obj = Address.objects.get(pk=address_id)
                address_obj.delete()
            logger.debug(ex)
            context = {"error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}

            return Response(context)


class AddAccount(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_user = []
            for i, f in enumerate(df, start=1):
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
                    address_qs = Address.objects.filter(id=user_detail_qs.address)[0]
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
                        print("address_serializer._errors", address_serializer._errors)
                        raise ValidationError(address_serializer.errors)

                        """ Auth user Data """

                    user_data = {
                            "first_name":f.get('first_name', None),
                            "last_name":f.get('last_name', None),
                            "email":f.get('email',None)

                    }

                    user_details_data = {
                            "user_obj":1,
                            "phone":f.get('phone', None),
                            "joining_date":f.get('joining_date', None),
                            "address":address_serializer.data['id'],
                    }

                    """  Pass dictionary through Context """
                    context = super().get_serializer_context()
                    context.update({"user_data": user_data,
                    "user_details_data":user_details_data})
                    try:
                        user_detail_serializer = AddUserSerializer(data=dict(user_data), context=context)

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
                        return Response(ex)

            keys = added_user[0].keys()
            with open('output.csv', 'w', newline='')  as output_file:
               dict_writer = csv.DictWriter(output_file, keys)
               dict_writer.writeheader()
               dict_writer.writerows(added_user)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            return Response(path_to_file)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            return Response(ex)


class AddSchool(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            print(df)
            added_school = []
            for i, f in enumerate(df, start=1):
                address_detail = {
                    "address": f.get('address', None),
                    "city": f.get('city', None),
                    "state": f.get('state', None),
                    "country": f.get('country', None),
                }

                licence_detail = {
                    "total_no_of_user": f.get('no._of_users', None),
                    "total_no_of_children": f.get('no_of_children', None),
                    "licence_from": f.get('licence_start', None),
                    # Need calculate from no. of month and licence start
                    "licence_till": f.get('no_of_month', None),
                }

                school_detail = {
                    "name": f.get('name', None),
                    "type": f.get('type', None),
                    "logo": f.get('logo', None),
                    "address": f.get('address', None),
                    "license": f.get('name', None)
                }

                school_package_detail = {
                    "school": f.get('school', None),
                    "package": f.get('package', None),
                    "from_date": f.get('from_date', None),
                    "to_date": f.get('to_date', None),
                    "custom_materials": f.get('custom_materials', None),

                }

                school_calender_detail = {
                    "school": f.get('school', None),
                    # Created AT ),
                    "session_from": f.get('session_from', None),
                    # calculate ),
                    "session_till": f.get('session_from', None),
                }

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            return Response(ex)


class AddSchoolGradeSubject(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_school_grade_subject = []

            for i, f in enumerate(df, start=1):
                # f['subject'] = list(f['subject'])
                f['subject'] = json.loads(f['subject'])
                print(f)
                schoolGradeSubject_serializer = SchoolGradeSubjectSerializer(
                    data=dict(f))
                if schoolGradeSubject_serializer.is_valid():
                    schoolGradeSubject_serializer.save()
                    added_school_grade_subject.append(
                        schoolGradeSubject_serializer.data)
                    print(schoolGradeSubject_serializer.data)
                else:
                    print("schoolGradeSubject_serializer._errors",
                          schoolGradeSubject_serializer._errors)
                    raise ValidationError(schoolGradeSubject_serializer.errors)

            keys = added_school_grade_subject[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_school_grade_subject)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            return Response(ex)
