"""
    DJANGO LIBRARY IMPORT
"""

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
            role_id = Role.objects.filter(name="Primary")[0].id
            print("role-------", role_id)
            user_detail_data = {
                "photo": request.data.get('photo', None),
                "phone": request.data.get('phone', None),
                "relationship_with_child": request.data.get('relationship_with_child', None),
                "role": [role_id],
                "is_platform_user":request.data.get('is_platform_user',None)
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
                # return Response(user_data_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            context = {'isSuccess': False, 'message': "Something went wrong",
                       'error': ex, "statusCode": status.HTTP_400_BAD_REQUEST}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
            # return Response(ex, status=status.HTTP_400_BAD_REQUEST)
from schools.models import*
from schools.api.edoofun_serializer import*
"""Get All ACCOUNT """


class GetAllAccounts(ListCreateAPIView):
    def post(self, request):

        try:
            print("@@@@@@@@@@@@",request.data )
            if request.data['type'] == 'account_id':
                print("account_id----")
                user_role_qs = UserRole.objects.filter(user=request.data.get('account_id',None))
                user_role_qs_serializer = SchoolUserRoleSerializers(user_role_qs, many=True)
                
                context = {'isSuccess': True, 'message': "School List by Account Id",
                           'data': user_role_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)

            elif request.data['type'] == 'school_id':
                print("35")
                
                school_qs = School.objects.filter(id = request.data.get('school_id',None))
                print("school_qs",school_qs)
                school_qs_serializer = SchoolListSerializer(school_qs, many=True)

                context = {'isSuccess': True, 'message': "School Detail by School Id",
                           'data': school_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            elif  request.data['type'] == 'all':
                roles = Role.objects.get(name='School Account Owner')
                roles = roles.id

                user_obj = UserDetail.objects.filter(role=roles)
                if user_obj:

                    user_obj_serializer = AccountUserSerializer(user_obj, many=True)

                    context = {'isSuccess': True, 'message': "Accounts List",
                            'data': user_obj_serializer.data, "statusCode": status.HTTP_200_OK}
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context = {'isSuccess': False, 'message': "Accounts List Not Found",
                            'data': user_obj_serializer.data, "statusCode": status.HTTP_404_NOT_FOUND}
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
            
            user_role = UserRole.objects.filter(school=pk).exclude(role=role_qs)
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
    def post(self,request):
        try:
            parent_detail = {
                "username": request.user.username,
                "email":request.data.get('parent_email', None),
                "old_pin":request.data.get('old_pin', None),
                "new_pin":request.data.get('new_pin', None)
            }
            
            context = super().get_serializer_context()
            context.update({"parent_detail": parent_detail})
            user_qs_serializer = UserChangePinSerializer(data=request.data, context=context)
            if user_qs_serializer.is_valid():
               
                context = {'isSuccess': True, 'message': "Pin changed Successfully",
                            "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {'isSuccess': False, 'message': "User Not Found",
                           'data': " ", "error":user_qs_serializer.errors,"statusCode": status.HTTP_404_NOT_FOUND}
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
                context = {'isSuccess': True, 'message': "Parent Detail",'data': user_qs_serializer.data,
                            "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, 'message': "Parent Detail Not Found",
                           'data': " ", "error":user_qs_serializer.errors,"statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print("EX", ex)
            print("traceback", traceback)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 





""" Get List Of Schools BasedOn AccountID """
class SchoolListByUser(GeneralClass,Mixins,ListCreateAPIView):
    model = UserRole
    filterset_class = UserRoleFilter

    def get(self, request, pk):
        try:
            user_school_qs = UserRole.objects.filter(user=pk).exclude(school__isnull =True)
            
            user_school_qs_serializer = SchoolListByUserSerializer(user_school_qs,many=True)
            return Response(user_school_qs_serializer.data,status=status.HTTP_200_OK)
        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
