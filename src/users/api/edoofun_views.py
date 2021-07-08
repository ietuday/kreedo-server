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
                "role": [role_id]
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
                # context = {'isSuccess': True, 'message': "Login Successfull",
                #            'data': user_data_serializer.data, "statusCode": status.HTTP_200_OK}
                # return Response(context, status=status.HTTP_200_OK)
                return Response(user_data_serializer.data, status=status.HTTP_200_OK)
            else:

                # context = {'isSuccess': False, "error": user_data_serializer.errors['non_field_errors'][0],
                #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
                # return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(user_data_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            # context = {'isSuccess': False, 'message': "Something went wrong",
            #            'error': ex, "statusCode": status.HTTP_400_BAD_REQUEST}
            # return Response(context,status=status.HTTP_400_BAD_REQUEST)
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)
