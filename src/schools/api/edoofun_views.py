from kreedo.conf.logger import CustomFormatter

from kreedo.conf import logger
import traceback

from .filters import*
from .edoofun_serializer import*
from schools.models import*
from django.shortcuts import render
"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework import status


""" ActiveSchoolList """
class ActiveSchoolList(ListCreateAPIView):
    def get(self, request):
        try:
            school_qs = School.objects.filter(is_active=True)
            
            if school_qs:
                school_qs_serializer = SchoolListSerializer(school_qs, many=True)
                context = {'isSuccess': True, 'message': "School List",
                            'data': school_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {'isSuccess': False, 'message': "School List Not Found",
                            'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print("@@@@@@@@", ex)
            print("TRACEBACK---", traceback.print_exc())
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            