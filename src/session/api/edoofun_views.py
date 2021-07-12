from kreedo.conf.logger import CustomFormatter

from kreedo.conf import logger
import traceback

from .filters import*
from .edoofun_serializer import*
from ..models import*
from django.shortcuts import render
"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework import status


""" get Section based on school """


class SectionListBySchool(ListCreateAPIView):
    def get(self, request, pk):
        try:
            section_qs = AcademicSession.objects.filter(school=pk)
            if section_qs:
                section_qs_serializer = SectionListBySchoolSerializer(
                    section_qs, many=True)


                context = {'isSuccess': True, 'message': "Section List",
                           'data': section_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': True, 'message': "Section List Not Found",
                           'data': " ", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:

            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




