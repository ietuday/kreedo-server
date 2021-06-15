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
        # if self.request.method == 'POST':
        #     return AcademicSessionCreateSerializer

    def post(self, request):
        try:
            grade_list = request.data.get('grade_list')
            print(grade_list)
            for grade in grade_list:
            
                academic_calender_qs = AcademicCalender.objects.filter(id=grade['academic_calender'])[0]
                grade['session_from']= academic_calender_qs.start_date
                grade['session_till']= academic_calender_qs.end_date

            academic_session_serializer = AcademicSessionCreateSerializer(
                data=request.data.get('grade_list'), many=True)

            if academic_session_serializer.is_valid():
                academic_session_serializer.save()
                return Response(academic_session_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(academic_session_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print("ERROR--->", ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" Appply Holiday List in Academic Session """
class ApplyAcademicCalenderToAcademicSession(GeneralClass, Mixins,CreateAPIView):
    def get(self, request, pk):
        try:
            academic_sesion_qs = AcademicSession.objects.get(id=pk)
            print("academic_sesion_qs---------->",academic_sesion_qs.academic_calender)
            print("@@---------->",academic_sesion_qs.id)

            holiday_qs = SchoolHoliday.objects.filter(academic_calender = academic_sesion_qs.academic_calender)
            print("@@@@@@@@@@@@@@@@", holiday_qs)

            for holiday in holiday_qs:
                holiday_id = holiday.holiday_type.id
                holiday_by_academic_calender = {
                    "academic_session": [academic_sesion_qs.id],
                    "title": holiday.title,
                    "description": holiday.description,
                    "holiday_from": holiday.holiday_from,
                    "holiday_till": holiday.holiday_till,
                    "holiday_type": holiday_id,
                    "is_active": holiday.is_active
                }
                print("holiday_by_academic_calender---------", holiday_by_academic_calender)

                school_holiday_serializer = SchoolHolidayCreateSerializer(
                    data=holiday_by_academic_calender)
                if school_holiday_serializer.is_valid():
                    school_holiday_serializer.save()
                else:

                    raise ValidationError(school_holiday_serializer.errors)
            week_off_by_academic_calender = {
                "academic_session":academic_sesion_qs.id,
                "monday": "false",
                "tuesday": "false",
                "wednesday": "false",
                "thursday": "false",
                "friday": "false",
                "saturday": "false",
                "sunday": "false",
                "is_active": "true"

            }
            print("week_off_by_academic_calender----",week_off_by_academic_calender)
            week_off_qs_serializer = SchoolWeakOffCreateSerializer(
                data=week_off_by_academic_calender)
            if week_off_qs_serializer.is_valid():
                week_off_qs_serializer.save()
            else:

                raise ValidationError(week_off_qs_serializer.errors)
            return Response("Academic Session Apply to Section", status=status.HTTP_200_OK)
            

        except Exception as ex:
            print("ERROR--->", ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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


class AcademicCalenderListCreate(GeneralClass, Mixin, ListCreateAPIView):
    model = AcademicCalender
    filterset_class = AcademicCalenderFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicCalenderListSerializer
        if self.request.method == 'POST':
            return AcademicCalenderCreateSerializer


""" Get Academic Session According to School ID """


class AcademicSessionBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            academic_session_qs = AcademicSession.objects.filter(
                session__school=request.data.get('session', None))
            academic_session_serializer = AcademicSessionListSerializer(
                academic_session_qs, many=True)
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


""" According to school get list of academic calender list"""


class AcademicCalenderListBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:

            academic_calender_qs = SchoolCalendar.objects.filter(school=pk)

            academic_calender_serializer = AcademicCalenderBySchoolSerializer(
                academic_calender_qs, many=True)

            return Response(academic_calender_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" According to school get list of grades and section list """


class GradeAndSectionListBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:

            resultant_dict = {}
            grade_qs = SchoolGradeSubject.objects.filter(
                school=request.data.get('school', None)).values('grade')

            grade_list = list(
                set(val for dic in grade_qs for val in dic.values()))

            grade_qs = Grade.objects.filter(id__in=grade_list)

            grade_qs_serializer = GradeListSerializer(grade_qs, many=True)

            return Response(grade_qs_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERROR-------", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateCalenderToPdf(ListCreateAPIView):

    def post(self, request):
        try:

            """
                Filter School ID From School Model
            """
            school_qs = School.objects.get(
                id=request.data.get('school_id', None)).id

            """ 
                Filter School ID From ACADEMIC CALENDER Model for getting no. of years
            """
            school_academic_calender_qs = SchoolCalendar.objects.filter(
                school=school_qs)

            for school_academic_calender_year in school_academic_calender_qs:
                """ get date list """
                date_list = Genrate_Date_of_Year(
                    school_academic_calender_year.session_from, school_academic_calender_year.session_till)
                """ get month list """
                month_list = Genrate_Month(
                    school_academic_calender_year.session_from, school_academic_calender_year.session_till)

            """ Get Week off list from SchoolWeakOff model """
            school_week_off = SchoolWeakOff.objects.filter(school=school_qs)
            school_week_off_serializer = SchoolWeakOffListSerializer(
                school_week_off, many=True)
            print("SCHOOL WEEK OFF", school_week_off_serializer.data)

            """ School holiday list from SchoolHoliday model"""
            school_holiday_qs = SchoolHoliday.objects.filter(
                school_session__school=school_qs)
            print("School holiday QS---->", school_holiday_qs)
            school_holiday_serailizer = SchoolHolidayListSerializer(
                school_holiday_qs, many=True)
            print("SCHOOL HOLIDAY ", school_holiday_serailizer.data)

        except Exception as ex:
            print("ERROR----->", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
