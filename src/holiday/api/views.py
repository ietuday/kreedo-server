from django.shortcuts import render

from .serializer import*
from holiday.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from .filters import*
# Create your views here.

""" School Holiday List and create """


class SchoolHolidayListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolHoliday
    filterset_class = SchoolHolidayFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolHolidayListSerializer
        if self.request.method == 'POST':
            return SchoolHolidayCreateSerializer


""" School Holiday Reetrive Update delete """


class SchoolHolidayRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SchoolHoliday
    serializer_class = SchoolHolidayCreateSerializer
    filterset_class = SchoolHolidayFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolHolidayListSerializer
        if self.request.method == 'PUT':
            return SSchoolHolidayCreateSerializer


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


""" Create Calendar """


class Calendar(ListCreateAPIView):
    def post(self, request):
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)

        calendar_data = SchoolHoliday.objects.filter(
            holiday_from__gte=start_date, holiday_till__gte=end_date, is_active=True)
        print("Calendar", calendar_data)

        # calendar_data = SchoolHoliday.objects.filter(
        #     holiday_from__range=[start_date, end_date])

        # print("Calendar", calendar_data)
        list = []

        for calendar_obj in calendar_data:
            dict = {}
            dict['id'] = calendar_obj.id
            dict['name'] = calendar_obj.name
            dict['description'] = calendar_obj.description
            # dict['academic_session'] = calendar_obj.academic_session
            dict['holiday_from'] = calendar_obj.holiday_from
            dict['holiday_till'] = calendar_obj.holiday_till
            dict['is_active'] = calendar_obj.is_active
            dict['type'] = calendar_obj.type
            list.append(dict)
            print("list", list)

        return Response(list)

        # calendar_serializer = CalendarSerializer(data=request.data)
        # if calendar_serializer.is_valid():
        #     print("Calendar", calendar_serializer.data)
        # else:
        #     print("Error", calendar_serializer.errors)
