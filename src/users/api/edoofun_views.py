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
from .edoofun_serializer import*


""" Create Log for Edoo-Fun  Serializer"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("Serailizer CAlled ")


"""  Register Parent """


class RegisterParent(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            # print(requjest)
            user_data = {
                "username": "test",
                "first_name": request.data.get('first_name', None),
                "last_name": request.data.get('last_name', None),
                "email": request.data.get('email', None)
            }

            user_detail_data = {
                "photo": request.data.get('photo', None),
                "phone": request.data.get('phone', None),
                "relationship_with_child": request.data.get('relationship_with_child', None),
            }

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"user_data": user_data, "user_detail_data": user_detail_data})

            user_detail_serialzer = RegisterParentSerializer(
                data=dict(user_data), context=context)
  

            if user_detail_serialzer.is_valid():
                user_detail_serialzer.save()
                return Response(user_detail_serialzer.data, status=status.HTTP_200_OK)
            else:
                print("user_detail_serialzer.errors------>", user_detail_serialzer.errors)
                logger.debug(user_detail_serialzer.errors)
                return Response(user_detail_serialzer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print("Error------>", ex)
            print("TRACEBACK---------->", traceback.print_exc())
            logger.debug(ex)

            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




