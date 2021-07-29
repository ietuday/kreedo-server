from django.shortcuts import render

from .serializer import*
from holiday.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

import pandas as pd
import csv
from users.api.custum_storage import FileStorage
from rest_framework.response import Response
from .filters import*
from rest_framework import status
# Create your views here.

""" holiday type list """


class HolidayTypeListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = HolidayType

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return HolidayTypeListSerializer
        if self.request.method == 'POST':
            return HolidayTypeListSerializer


""" School Holiday List and create """


class SchoolHolidayListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolHoliday
    filterset_class = SchoolHolidayFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolHolidayListSerializer
        if self.request.method == 'POST':
            return SchoolHolidayCreateSerializer


""" SchoolHolidayListBySchool """


class SchoolHolidayListBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:
            school_holiday_qs = SchoolHoliday.objects.filter(school=pk)
            if school_holiday_qs:
                school_holiday_qs_serializer = SchoolHolidayListSerializer(
                    school_holiday_qs, many=True)
                return Response(school_holiday_qs_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Holiday List Not Found", status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" School Holiday Retrive Update delete """


class SchoolHolidayRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SchoolHoliday
    serializer_class = SchoolHolidayCreateSerializer
    filterset_class = SchoolHolidayFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolHolidayListSerializer
        if self.request.method == 'PUT':
            return SchoolHolidayCreateSerializer
        if self.request.method == 'PATCH':
            return SchoolHolidayCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" School Weak off List and create """


class SchoolWeakOffListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolWeakOff
    filterset_class = SchoolWeakOffFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolWeakOffListSerializer
        if self.request.method == 'POST':
            return SchoolWeakOffCreateSerializer


""" School Weak off Retrive Update Delte """


class SchoolWeakOffRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateAPIView):
    model = SchoolWeakOff
    filterset_class = SchoolWeakOffFilter
    serializer_class = SchoolWeakOffCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolWeakOffListSerializer
        if self.request.method == 'PUT':
            return SchoolWeakOffCreateSerializer


""" School Week off By Academic Session """


class SchoolWeakOffByAcademicSession(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:

            school_week_qs = SchoolWeakOff.objects.filter(academic_session=pk)
            if school_week_qs:
                school_week_qs_serializer = SchoolWeakOffListSerializer(
                    school_week_qs, many=True)
                return Response(school_week_qs_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Week-Off Not Found", status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" School Holiday List By Academic Session """


class HolidayListByAcademicSession(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:
            holiday_qs = SchoolHoliday.objects.filter(academic_session=pk)
            print("holiday_qs", holiday_qs)
            if holiday_qs:
                holiday_qs_serializer = SchoolHolidayListSerializer(
                    holiday_qs, many=True)
                return Response(holiday_qs_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Holiday List Not Found", status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Create Calendar """


class Calendar(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)

            calendar_data = SchoolHoliday.objects.filter(
                holiday_from__gte=start_date, holiday_till__gte=end_date, is_active=True)
            print("Calendar", calendar_data)
            calendar_data_qs = SchoolHolidayListSerializer(
                calendar_data, many=True)
            return Response(calendar_data_qs.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # list = []

        # for calendar_obj in calendar_data:
        #     dict = {}
        #     dict['id'] = calendar_obj.id
        #     dict['name'] = calendar_obj.name
        #     dict['description'] = calendar_obj.description
        #     # dict['academic_session'] = calendar_obj.academic_session
        #     dict['holiday_from'] = calendar_obj.holiday_from
        #     dict['holiday_till'] = calendar_obj.holiday_till
        #     dict['is_active'] = calendar_obj.is_active
        #     dict['type'] = calendar_obj.type
        #     list.append(dict)
        #     print("list", list)

        # return Response(list,status=status.HTTP_200_OK)

        # calendar_serializer = CalendarSerializer(data=request.data)
        # if calendar_serializer.is_valid():
        #     print("Calendar", calendar_serializer.data)
        # else:
        #     print("Error", calendar_serializer.errors)


""" School Calender according to start date and type """


class HolidayListByType(GeneralClass, Mixins, ListCreateAPIView):

    def post(self, request):
        try:
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)
            type = request.data.get('type', None)

            if type:
                querset = SchoolHoliday.objects.filter(
                    school_session=type, holiday_from__gte=start_date, holiday_till__lte=end_date)
            elif type:
                querset = SchoolHoliday.objects.filter(
                    academic_calender=type, holiday_from__gte=start_date, holiday_till__lte=end_date)
            elif type:
                querset = SchoolHoliday.objects.filter(
                    academic_session=type, holiday_from__gte=start_date, holiday_till__lte=end_date)

            holiday_serializer = SchoolHolidayListSerializer(
                querset, many=True)
            return Response(holiday_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Holiday List of month  According to School """


class HolidayListOfMonthBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            school_holiday_qs = SchoolHoliday.objects.filter(holiday_from__year=request.data.get('year', None),
                                                             holiday_from__month=request.data.get('month', None), school=request.data.get('school', None))

            school_holiday_qs_serializer = SchoolHolidaySerializer(
                school_holiday_qs, many=True)
            return Response(school_holiday_qs_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Holiday List of month  According to Academic Session """


class HolidayListOfMonthByAcademicSession(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            school_holiday_qs = SchoolHoliday.objects.filter(holiday_from__year=request.data.get('year', None),
                                                             holiday_from__month=request.data.get('month', None), academic_session=request.data.get('academic_session', None))

            school_holiday_qs_serializer = SchoolHolidaySerializer(
                school_holiday_qs, many=True)
            return Response(school_holiday_qs_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:

            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Week off by  academic_calender """


class WeekOffByAcademicCalender(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:

            week_off_qs = SchoolWeakOff.objects.filter(academic_calender=pk)
            if week_off_qs:
                week_off_qs_serializer = SchoolWeakOffListSerializer(
                    week_off_qs[0])
                return Response(week_off_qs_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("", status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Week off by  academic_session """


class WeekOffByAcademicSession(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:

            week_off_qs = SchoolWeakOff.objects.filter(academic_session=pk)
            if week_off_qs:
                week_off_qs_serializer = SchoolWeakOffListSerializer(
                week_off_qs[0])
                return Response(week_off_qs_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("", status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:

            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Holiday List According to  month , year , academic_calender id """


class HolidayListOfMonthByAcademicCalender(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            school_holiday_qs = SchoolHoliday.objects.filter(holiday_from__year=request.data.get('year', None),
                                                             holiday_from__month=request.data.get('month', None), academic_calender=request.data.get('academic_calender', None))

            school_holiday_qs_serializer = SchoolHolidaySerializer(
                school_holiday_qs, many=True)
            return Response(school_holiday_qs_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERROR----", ex)

            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Download Calender of School holiday """


class DownloadListOfHolidaysInCSVBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        type = request.data.get('type', None)
        try:
            holiday_list = []
            if type == 'school':
                school_holiday_qs = SchoolHoliday.objects.filter(
                    school=request.data.get('school', None))
                school_id = request.data.get('school', None)

            elif type == 'academic_calender':
                school_holiday_qs = SchoolHoliday.objects.filter(
                    academic_calender=request.data.get('academic_calender', None))
                school_id = request.data.get('academic_calender', None)

            elif type == 'academic_session':
                school_holiday_qs = SchoolHoliday.objects.filter(
                    academic_session=request.data.get('academic_session', None))
                school_id = request.data.get('academic_session', None)

            for data in school_holiday_qs:

                holiday_list.append(
                    {
                        "title": data.title,
                        "description": data.description,
                        "holiday_from": data.holiday_from,
                        "holiday_till": data.holiday_till,
                        "holiday_type": data.holiday_type,
                        "is_active": data.is_active
                    }
                )

            keys = holiday_list[0].keys()
            name = str(school_id) + '-' 'holiday_list'+'.csv'
            with open(name, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(holiday_list)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                name, 'kreedo-new', 'files/'+name)
            path_to_file = 'https://' + str(fs.custom_domain) + '/files/'+name
            print(path_to_file)
            return Response(path_to_file, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
