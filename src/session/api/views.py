from .filters import *
import json
from .serializer import*
from schools.models import*
from kreedo.general_views import *
from django.shortcuts import render
"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework import status

# Create your views here.

""" School Session Create  and list """


class SchoolSessionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolSession
    filterset_class = SchoolSessionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolSessionListSerializer
        if self.request.method == 'POST':
            return SchoolSessionCreateSerializer


""" School Session Retrive Update Delete """


class SchoolSessionRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SchoolSession
    filterset_class = SchoolSessionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolSessionListSerializer
        if self.request.method == 'PUT':
            return SchoolSessionCreateSerializer
        if self.request.method == 'DELETE':
            return SchoolSessionCreateSerializer


""" AcademicSession Create  and list """


class AcademicSessionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = AcademicSession
    filterset_class = AcademicSessionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicSessionListSerializer
        if self.request.method == 'POST':
            return AcademicSessionCreateSerializer


""" AcademicSession Retrive Update Delete """


class AcademicSessionRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = AcademicSession
    filterset_class = AcademicSessionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicSessionListSerializer
        if self.request.method == 'PUT':
            return AcademicSessionCreateSerializer
        if self.request.method == 'DELETE':
            return AcademicSessionListSerializer


""" Create and List of Academic Calender """


class AcademicCalenderListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = AcademicCalender
    filterset_class = AcademicCalenderFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicCalenderListSerializer
        if self.request.method == 'POST':
            return AcademicCalenderCreateSerializer


""" Retrive Update and Delete Academic Calender """


class AcademicCalenderRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = AcademicCalender
    filterset_class = AcademicCalenderFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicCalenderListSerializer
        if self.request.method == 'PUT':
            return AcademicCalenderCreateSerializer
        if self.request.method == 'DELETE':
            return AcademicCalenderListSerializer


class AcademicSessionByTeacher(ListCreateAPIView):

    def post(self, request):
        try:
            class_teacher = request.data.get('class_teacher', None)
            if class_teacher is not None:
                academicSession_qs = AcademicSession.objects.filter(
                    class_teacher=class_teacher)
                aca_session_qs = AcademicSessionListSerializer(
                    academicSession_qs, many=True)
                context = {"message": "Academic Session By Teacher",
                           "statusCode": status.HTTP_200_OK, "isSucess": True, "data": aca_session_qs.data}
                return Response(context)
            else:
                context = {"error": "Teacher Not Found",  "isSucess": False,
                           "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(context)

        except Exception as ex:
            logger.debug(ex)
            context = {"error": ex, "isSucess": False,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}

            return Response(context)
