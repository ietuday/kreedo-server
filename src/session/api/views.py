from .filters import *
import json
from .serializer import*
from schools.models import*
from kreedo.general_views import *
from django.shortcuts import render

from .utils import*
from holiday.models import*
from holiday.api.serializer import*

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
        if self.request.method == 'PATCH':
            return SchoolSessionCreateSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)



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
        if self.request.method == 'PATCH':
            return AcademicSessionCreateSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Create and List of Academic Calender """


class AcademicCalenderListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = AcademicCalender
    filterset_class = AcademicCalenderFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicCalenderListSerializer
        if self.request.method == 'POST':
            return AcademicCalenderCreateSerializer





""" Get Academic Session According to School ID """
class AcademicSessionBySchool(GeneralClass,Mixins,ListCreateAPIView):
    def post(self, request):
        try:
            academic_session_qs = AcademicSession.objects.filter(session__school=request.data.get('school',None))
            academic_session_serializer = AcademicSessionListSerializer(academic_session_qs,many=True)
            return Response(academic_session_serializer.data, status=status.HTTP_200_OK)
    
        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" Retrive Update and Delete Academic Calender """


class AcademicCalenderRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = AcademicCalender
    filterset_class = AcademicCalenderFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicCalenderListSerializer
        if self.request.method == 'PUT':
            return AcademicCalenderCreateSerializer
        if self.request.method == 'PATCH':
            return AcademicCalenderCreateSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class AcademicSessionByTeacher(GeneralClass, Mixins, ListCreateAPIView):

    def post(self, request):
        try:
            class_teacher = request.data.get('class_teacher', None)
            if class_teacher is not None:
                academicSession_qs = AcademicSession.objects.filter(
                    class_teacher=class_teacher)
                aca_session_qs = AcademicSessionListSerializer(
                    academicSession_qs, many=True)
                # context = {"message": "Academic Session By Teacher",
                #            "statusCode": status.HTTP_200_OK, "isSucess": True, "data": aca_session_qs.data}
                return Response(aca_session_qs.data, status=status.HTTP_200_OK)
            else:
                # context = {"error": "Teacher Not Found",  "isSucess": False,
                #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
                return Response(aca_session_qs.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            logger.debug(ex)
            # context = {"error": ex, "isSucess": False,
            #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}

            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateCalenderToPdf(ListCreateAPIView):

    def post(self,request):
        try:

            """ 
                Filter School ID From School Model 
            """
            school_qs = School.objects.get(id=request.data.get('school_id', None)).id

            """ 
                Filter School ID From ACADEMIC CALENDER Model for getting no. of years
            """
            school_academic_calender_qs = SchoolCalendar.objects.filter(school=school_qs)
            print("ACADEMIC CALENDER--->",school_academic_calender_qs)

            for school_academic_calender_year in school_academic_calender_qs:
                """ get date list """ 
                date_list = Genrate_Date_of_Year(school_academic_calender_year.session_from,school_academic_calender_year.session_till)
                print("DATE----->",date_list)
                """ get month list """
                month_list = Genrate_Month(school_academic_calender_year.session_from,school_academic_calender_year.session_till)
                print("MONTH------>", month_list)


            """ Get Week off list from SchoolWeakOff model """
            school_week_off = SchoolWeakOff.objects.filter(school=school_qs)
            school_week_off_serializer = SchoolWeakOffListSerializer(school_week_off,many=True)
            print("SCHOOL WEEK OFF", school_week_off_serializer.data)

            """ School holiday list from SchoolHoliday model"""
            school_holiday_qs = SchoolHoliday.objects.filter(school_session__school=school_qs)
            print("School holiday QS---->", school_holiday_qs)
            school_holiday_serailizer = SchoolHolidayListSerializer(school_holiday_qs, many=True)
            print("SCHOOL HOLIDAY ", school_holiday_serailizer.data)




        except Exception as ex:
            print("ERROR----->", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
