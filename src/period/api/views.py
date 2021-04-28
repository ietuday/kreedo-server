from django.shortcuts import render
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from kreedo.general_views import*
from period.models import *
from .filters import*
from .serializer import *
from rest_framework.response import Response
from holiday.models import*
from .utils import*
# Create your views here.
""" Period Template List and Create """


class PeriodTemplateListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = PeriodTemplate
    filterset_class = PeriodTemplateFilter
    serializer_class = PeriodTemplateSerializer


""" Period Template Retrive Update """


class PeriodTemplateRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = PeriodTemplate
    filterset_class = PeriodTemplateFilter
    serializer_class = PeriodTemplateSerializer


""" Period List and Create """


class PeriodListCreate(ListCreateAPIView):
    # model = Period
    # filterset_class = PeriodFilter

    def post(self, request):
        try:

            grade_list = request.data.get("grade_list")

            for grade in grade_list:
                """ Get Holidays Function Call """
                school_holiday_count = school_holiday(grade)

                """ Get Weak-off Function Call """
                week_off = weakoff_list(grade)
                count_weekday = weekday_count(grade, week_off)
                working_days = total_working_days(grade,count_weekday)
                create_period(grade)
                return Response(working_days)

        except Exception as ex:
            print("ERRROR", ex)
            return Response(ex)


""" Period Retrive and Update"""


class PeriodRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Period
    filterset_class = PeriodFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PeriodListSerializer
        if self.request.method == 'PUT':
            return PeriodCreateSerializer
        if self.request.method == 'DELETE':
            return PeriodListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PeriodListSerializer
        if self.request.method == 'POST':
            return PeriodCreateSerializer
        if self.request.method == 'DELETE':
            return PeriodListSerializer


"""PeriodTemplateDetail List and Create """


class PeriodTemplateDetailListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = PeriodTemplateDetail
    filterset_class = PeriodTemplateDetailFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PeriodTemplateDetailListSerializer
        if self.request.method == 'POST':
            return PeriodTemplateDetailCreateSerializer


""" Period Template Detail Retrive Update """


class PeriodTemplateDetailRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = PeriodTemplateDetail
    filterset_class = PeriodTemplateDetailFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PeriodTemplateDetailListSerializer
        if self.request.method == 'PUT':
            return PeriodTemplateDetailCreateSerializer
