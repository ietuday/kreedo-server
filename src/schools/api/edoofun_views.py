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
           
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



class GetListOfAllSchools(ListCreateAPIView):
    model = School
    filterset_class = SchoolFilter

    def get(self, request):
        try:
            school_qs = School.objects.all()
            

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
           
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



""" Section Retrive Update delete """


class GetSchoolDetailsBasedOnSchoolID(RetrieveUpdateDestroyAPIView):
    model = School
    filterset_class = SchoolFilter

    def get(self, request, pk):
        try:
            school_qs = School.objects.filter(id=pk)
        
            if school_qs:
                school_qs_serializer = SchoolDetailListSerializer(school_qs, many=True)
                context = {'isSuccess': True, 'message': "School Detail by School Id",
                            'data': school_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {'isSuccess': False, 'message': "School Detail by School Id Not Found",
                            'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
           
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

"""GetListOfSchoolsBasedOnAccountID"""

class GetListOfSchoolsBasedOnAccountID(RetrieveUpdateDestroyAPIView):
    model = School
    filterset_class = SchoolFilter

    def post(self, request):
        try:
            
            school_qs = School.objects.filter(account_manager=request.data.get('account_id',None),
                         is_active=request.data.get('status',None))
        
            if school_qs:
                school_qs_serializer = SchoolDetailSerializer(school_qs, many=True)
                context = {'isSuccess': True, 'message': "List Of Schools Based On Account ID",
                            'data': school_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {'isSuccess': False, 'message': "List Of Schools Based On Account ID Not Found",
                            'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
           
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            