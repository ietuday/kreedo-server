from .filters import *
import json
from .serializer import*
from schools.models import*
from kreedo.general_views import *
from django.shortcuts import render
from django.db.models import Q



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
                return Response(academic_session_serializer.errors, status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERROR--->", ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" Grade List by Academic Calender """


class GradeLisbyAcademicSession(GeneralClass,Mixins,ListCreateAPIView):
    def get(self,request, pk):
        try:
            academic_sesion_qs = AcademicSession.objects.filter(academic_calender=pk)
            academic_sesion_qs_serializer = AcademicSessionForGradeSerializer(academic_sesion_qs, many=True)
            return Response(academic_sesion_qs_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print("ERROR--->", ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" Academic Calender by School """

class AcademicCalenderBySchool(GeneralClass,Mixins,ListCreateAPIView):
    def get(self,request, pk):
        try: 
            academic_calender_qs = AcademicCalender.objects.filter(school=pk)
            academic_calender_qs_serializer = AcademicCalenderListSerializer(academic_calender_qs, many=True)
            return Response(academic_calender_qs_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print("ERROR--->", ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Apply Holiday List in Academic Session """
class ApplyAcademicCalenderToAcademicSession(GeneralClass, Mixins,CreateAPIView):
    def get(self, request, pk):
        try:
            academic_sesion_qs = AcademicSession.objects.get(id=pk)
            academic_id = academic_sesion_qs.id
         
            holiday_qs = SchoolHoliday.objects.filter(academic_calender = academic_sesion_qs.academic_calender)
  
            for holiday in holiday_qs:
              
                holiday_id = holiday.holiday_type.id
              
                holiday_by_academic_calender = {
                    "academic_session": academic_id,
                    "title": holiday.title,
                    "description": holiday.description,
                    "holiday_from": holiday.holiday_from,
                    "holiday_till": holiday.holiday_till,
                    "holiday_type": holiday_id,
                    "is_active": holiday.is_active
                }

                school_holiday_serializer = SchoolHolidayCreateSerializer(
                    data=holiday_by_academic_calender)
                if school_holiday_serializer.is_valid():
                    school_holiday_serializer.save()
                else:
                    print("school_holiday_serializer.errors",school_holiday_serializer.errors)
                    raise ValidationError(school_holiday_serializer.errors)
            week_off_qs = SchoolWeakOff.objects.filter(academic_calender=academic_sesion_qs.academic_calender)
            for week in week_off_qs:

                week_off_by_academic_calender = {
                    "academic_session":academic_id,
                    "monday": week.monday,
                    "tuesday": week.tuesday,
                    "wednesday": week.wednesday,
                    "thursday": week.thursday,
                    "friday": week.friday,
                    "saturday": week.saturday,
                    "sunday": week.sunday,
                    "is_active": week.is_active

                }
                week_off_qs_serializer = SchoolWeakOffCreateSerializer(
                    data=week_off_by_academic_calender)
                if week_off_qs_serializer.is_valid():
                    week_off_qs_serializer.save()
                else:

                    raise ValidationError(week_off_qs_serializer.errors)
            academic_sesion_qs.is_applied="True"
            academic_sesion_qs.save()
            return Response("Academic Session Apply to Section", status=status.HTTP_200_OK)
            

        except Exception as ex:
            print("ERROR-------", ex)
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

""" Academic Calender and Grade List """
class ClassTeacherByAcademicCalenderGrade(GeneralClass,Mixins, ListCreateAPIView):
    def post(self,request):
        try:
            acadmic_session_qs = AcademicSession.objects.filter(grade=request.data.get('grade', None),
                                academic_calender = request.data.get('academic_calender', None))
            academic_session_serializer = ClassTeacherByAcademicSession(acadmic_session_qs, many=True)
            return Response(academic_session_serializer.data, status=status.HTTP_200_OK)


        except Exception as ex:
            print("ERROR-------", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" School Calender PDF """ 

class GenerateCalenderToPdf(ListCreateAPIView):

    def get(self, request,pk):
        try:

            # school_qs = School.objects.get(
            #     id=pk).id

            school_academic_calender_qs = AcademicCalender.objects.filter(
                school=pk)
            calender_list = []
            calender_dict = {}
            print("school_academic_calender_qs", school_academic_calender_qs)
            for school_academic_calender_year in school_academic_calender_qs:
                
                """ get date list """
                calender_dict['date_list'] = Genrate_Date_of_Year(
                    school_academic_calender_year.start_date, school_academic_calender_year.end_date)
                # print("Date--------", date_list)

                """ get month list """
                calender_dict['month_list'] = Genrate_Month(
                    school_academic_calender_year.start_date, school_academic_calender_year.end_date)
                # print("Month------------>")
                calender_list.append(calender_dict)

            """ Get Week off list from SchoolWeakOff model """
            school_week_off = SchoolWeakOff.objects.filter(school=pk)
            school_week_off_serializer = SchoolWeakOffListSerializer(
                school_week_off, many=True)
            print("SCHOOL WEEK OFF", school_week_off_serializer.data)
            # calender_list['school_week_off'] = school_week_off_serializer.data

            """ School holiday list from SchoolHoliday model"""
            school_holiday_qs = SchoolHoliday.objects.filter(school=pk)
            print("School holiday QS---->", school_holiday_qs)

            school_holiday_serailizer = SchoolHolidayListSerializer(
                school_holiday_qs, many=True)
            print("SCHOOL HOLIDAY ", school_holiday_serailizer.data)
            # calender_list['school_holiday_list'] = school_holiday_serailizer.data
            
            return Response(calender_list)
        except Exception as ex:
            print("ERROR----->", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AssociateAcademicSession(RetrieveUpdateDestroyAPIView):

    def patch(self, request,pk):
        try:
            acad_data = {
                "session": request.data.get('session', None),
                "grade": request.data.get('session', None),
                "section": request.data.get('section', None),
                "class_teacher": request.data.get('class_teacher', None),
                "subjects": request.data.get('subjects', None),
            }
            acad_session_qs = AcademicSession.objects.filter(id=pk)
            academic_session_qs = AcademicSessionCreateSerializer(acad_session_qs,data=dict(acad_data), partial=True)
            subject_teacher_list = request.data.get('subject_teacher_list', None)
            for sub_tech in subject_teacher_list:
                sub_tech_qs = SectionSubjectTeacher.objects.create(sub_tech)
            
            return Response(academic_session_qs.data, status=status.HTTP_200_OK)


        except Exception as ex:
            print("ERROR----->", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import datetime

class DownloadCalendar(ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        try:
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)
            # print(Genrate_Month(start_date, end_date))
            calendar_type = request.data.get('calendar_type', None)
            school = request.data.get('school', None)
            grade = request.data.get('grade', None)
            section = request.data.get('section', None)
            
            result =  {}
            result['days'] = ['M', 'T', 'W', 'T', 'F', 'S', 'S', 'M', 'T', 'W', 'T', 'F', 'S', 'S', 'M', 'T', 'W', 'T', 'F', 'S', 'S', 'M', 'T', 'W', 'T', 'F', 'S', 'S', 'M', 'T', 'W', 'T', 'F', 'S', 'S']
            months_list = ["", "Jan", "Feb", "Mar", "Apr","May", "Jun", "Jul", "Aug", "Sep", "Oct",  "Nov", "Dec"]
            generated_month_list = Genrate_Month(start_date, end_date)
            print("generated_month_list",generated_month_list)
            if calendar_type == 'school-calender':
                school_calender_qs = SchoolCalendar.objects.filter(school=school)
                if len(school_calender_qs) is not 0:
                    # print(school_calender_qs[0].id)
                    school_calender_holiday_qs = SchoolHoliday.objects.filter(school_calender=school_calender_qs[0].id,school=school)
                    schoolHolidayListSerializer = SchoolHolidaySerializer(school_calender_holiday_qs, many=True)
                    # print(school_calender_holiday_qs)
                    result['holidays'] = schoolHolidayListSerializer.data
                    start_date_time_obj = datetime.datetime.strptime(start_date, '%d-%m-%Y')
                    end_date_time_obj = datetime.datetime.strptime(end_date, '%d-%m-%Y')

                    months = []
                    for dt in daterange(start_date_time_obj, end_date_time_obj):
                        if months_list[dt.date().month] + "-" + str(dt.date().year) in generated_month_list:
                            print(months_list[dt.date().month] + "-" + str(dt.date().year))
                            month_dict = {
                                "month": months_list[dt.date().month] + "-" + str(dt.date().year),
                                "days": [],
                            }
                            month_dict['days'].append({
                                        'date': dt.date(),
                                        'isHoliday': checkHoliday(dt.date(), schoolHolidayListSerializer.data),
                                        'holidayType': checkHolidayType(dt.date(), schoolHolidayListSerializer.data),
                                        'color': checkHolidayColor(dt.date(), schoolHolidayListSerializer.data),
                                        'isweekend': False,
                                        'isFirstDayofMonth': checkFirstDay(dt.date()),
                                        "weekday": dt.date().weekday(),
                                        "month": months_list[dt.date().month] + "-" + str(dt.date().year),
                                        "isStart": checkStartEndDate(dt.date(),school_calender_qs[0].session_from),
                                        "isEnd": checkStartEndDate(dt.date(),school_calender_qs[0].session_till)
                            })
                            months.append(month_dict)
                else:
                    context = {
                    "success": False, "message": "DownloadCalendar", "error": "SchoolCalendar for this School is not valid", "data": ""}
                    return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    
            elif calendar_type == 'section-calendar': 
                school_calender_qs = SchoolCalendar.objects.filter(school=school)
                acadamic_calender_qs = AcademicCalender.objects.filter(school=school)
                acadamic_session_qs = AcademicSession.objects.filter(grade=grade, section=section)
                if len(school_calender_qs) is not 0 and len(acadamic_calender_qs) is not 0 and len(acadamic_session_qs) is not 0:
                    school_calender_holiday_qs = SchoolHoliday.objects.filter(Q(school_calender=school_calender_qs[0].id)|Q(academic_calender=acadamic_calender_qs[0].id)| Q(academic_session=acadamic_session_qs[0].id))
                    schoolHolidayListSerializer = SchoolHolidaySerializer(school_calender_holiday_qs, many=True)
                    # print(school_calender_holiday_qs)
                    result['holidays'] = schoolHolidayListSerializer.data
                    start_date_time_obj = datetime.datetime.strptime(start_date, '%d-%m-%Y')
                    end_date_time_obj = datetime.datetime.strptime(end_date, '%d-%m-%Y')
                    school_week_off_qs = SchoolWeakOff.objects.filter(school=school,academic_calender= acadamic_calender_qs[0].id)
                    schoolWeakOffSerializer = SchoolWeakOffCreateSerializer(school_week_off_qs, many=True)

                    months = []
                    for dt in daterange(start_date_time_obj, end_date_time_obj):


                        if months_list[dt.date().month] + "-" + str(dt.date().year) in generated_month_list:
                            print(months_list[dt.date().month] + "-" + str(dt.date().year))
                            month_dict = {
                                "month": months_list[dt.date().month] + "-" + str(dt.date().year),
                                "days": [],
                            }
                            month_dict = {
                                'date': dt.date(),
                                'isHoliday': checkHoliday(dt.date(), schoolHolidayListSerializer.data),
                                'holidayType': checkHolidayType(dt.date(), schoolHolidayListSerializer.data),
                                'color': checkHolidayColor(dt.date(), schoolHolidayListSerializer.data),
                                'isweekend': checkWeekOff(dt.date(),schoolWeakOffSerializer.data ),
                                'isFirstDayofMonth': checkFirstDay(dt.date()),
                                "weekday": dt.date().weekday(),
                                "isStart": checkStartEndDate(dt.date(),school_calender_qs[0].session_from),
                                "isEnd": checkStartEndDate(dt.date(),school_calender_qs[0].session_till)
                            }
                            # print(month_dict)
                            months.append(month_dict)

                else:
                    context = {
                    "success": False, "message": "DownloadCalendar", "error": "academic-session-calendar for this School is not valid", "data": ""}
                    return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 


            elif calendar_type == 'academic-session-calendar':
                school_calender_qs = SchoolCalendar.objects.filter(school=school)
                acadamic_calender_qs = AcademicCalender.objects.filter(school=school)
                if len(school_calender_qs) is not 0 and len(acadamic_calender_qs) is not 0:
                    school_calender_holiday_qs = SchoolHoliday.objects.filter(Q(school_calender=school_calender_qs[0].id)|Q(academic_calender=acadamic_calender_qs[0].id))
                    schoolHolidayListSerializer = SchoolHolidaySerializer(school_calender_holiday_qs, many=True)
                    # print(school_calender_holiday_qs)
                    result['holidays'] = schoolHolidayListSerializer.data
                    start_date_time_obj = datetime.datetime.strptime(start_date, '%d-%m-%Y')
                    end_date_time_obj = datetime.datetime.strptime(end_date, '%d-%m-%Y')
                    school_week_off_qs = SchoolWeakOff.objects.filter(school=school,academic_calender= acadamic_calender_qs[0].id)
                    schoolWeakOffSerializer = SchoolWeakOffCreateSerializer(school_calender_holiday_qs, many=True)

                    months = []
                    for dt in daterange(start_date_time_obj, end_date_time_obj):
                        if months_list[dt.date().month] + "-" + str(dt.date().year) in generated_month_list:
                            print(months_list[dt.date().month] + "-" + str(dt.date().year))
                            month_dict = {
                                "month": months_list[dt.date().month] + "-" + str(dt.date().year),
                                "days": [],
                            }
                            month_dict = {
                                'date': dt.date(),
                                'isHoliday': checkHoliday(dt.date(), schoolHolidayListSerializer.data),
                                'holidayType': checkHolidayType(dt.date(), schoolHolidayListSerializer.data),
                                'color': checkHolidayColor(dt.date(), schoolHolidayListSerializer.data),
                                'isweekend': checkWeekOff(dt.date(),schoolWeakOffSerializer.data ),
                                'isFirstDayofMonth': checkFirstDay(dt.date()),
                                "weekday": dt.date().weekday(),
                                "isStart": checkStartEndDate(dt.date(),school_calender_qs[0].session_from),
                                "isEnd": checkStartEndDate(dt.date(),school_calender_qs[0].session_till)
                            }
                            # print(month_dict)
                            months.append(month_dict)

                else:
                    context = {
                    "success": False, "message": "DownloadCalendar", "error": "SchoolCalendar for this School is not valid", "data": ""}
                    return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
            else:
                context = {
                "success": False, "message": "DownloadCalendar", "error": "calendar type not valid", "data": ""}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # result['day'] = months_by_month(months,generated_month_list)
            result['day'] = months
            context = {
                "success": True, "message": "DownloadCalendar", "error": "", "data": result}

            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            context = {
                "success": False, "message": "Error", "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SchoolCalendarBySchool(RetrieveUpdateDestroyAPIView):
     def get(self, request,pk):
        try:
            school_calander_qs = SchoolCalendar.objects.filter(school=pk, is_active=True)
            if len(school_calander_qs) != 0:
                schoolCalendarCreateSerializer = SchoolCalendarCreateSerializer(school_calander_qs[0])
                context = {"isSuccess": True, "message": "School Calendar By School", "error": "", "data": schoolCalendarCreateSerializer.data}
                return Response(context, status=status.HTTP_200_OK)
            else: 
                context = {
                "isSuccess": False, "message": "School calander not vailable", "error": "", "data": ""}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except Exception as ex:
            print("ERROR----->", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

