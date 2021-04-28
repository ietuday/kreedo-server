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
                working_days = total_working_days(grade, count_weekday)
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


""" List of classes acording to teacher id , date, and day """


class ClassAccordingToTeacher(GeneralClass, ListCreateAPIView):
    serializer_class = ClassAccordingToTeacherSerializer

    def post(self, request):

        try:
            teacher = request.data['teacher']
            print("@@@@@@@@@@2", teacher[0])
            period_list = Period.objects.filter(
                teacher=teacher[0], start_date=request.data['start_date'])
            print("LIST", period_list)
            list = []
            dict = {}
            for class_period in period_list:
                dict['id'] = class_period.id
                dict['room_no'] = class_period.room_no
                dict['start_time'] = class_period.start_time
                dict['end_time'] = class_period.end_time
                # dict['grade'] = class_period.academic_session.grade
                activity_missed = GroupActivityMissed.objects.filter(
                    period=class_period.id).count()
                print("ACRIVITY MISSEd", activity_missed)
                dict['activity_behind'] = activity_missed
                print("DICT", dict)
                list.append(dict)
                data = list
            context = {"data": data}
            return Response(context)
            # class_teacher_serializer = ClassAccordingToTeacherSerializer(
            #     context={'request': request}, data=request.data)
            # if class_teacher_serializer.is_valid():

            #     print("@@@@@@",class_teacher_serializer.data)
            #     return Response(class_teacher_serializer.data)
            # else:
            #     print(class_teacher_serializer.errors)
            #     return Response(class_teacher_serializer.errors)

        except Exception as ex:
            print("ERror", ex)
            return Response(ex)
