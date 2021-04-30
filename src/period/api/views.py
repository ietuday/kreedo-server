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
from session.models import*
from session.api.serializer import*
from rest_framework import status
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


class ClassAccordingToTeacher(ListCreateAPIView):
    model = Period
    # serializer_class = ClassAccordingToTeacherSerializer

    def post(self, request):

        try:

            teacher = request.data.get('teacher', None)
            print("TEACHER----->", teacher)

            period_list_qs = Period.objects.filter(
                teacher=teacher[0], start_date=request.data.get('start_date'))

            print("##################", period_list_qs)

            periods_lists = []
            dict = {}
            for class_period in period_list_qs:
                dict['period_id'] = class_period.id
                dict['room_no'] = class_period.room_no.room_no
                dict['start_time'] = class_period.start_time
                dict['end_time'] = class_period.end_time
                academic_session = class_period.academic_session.all()
                acad_session = AcademicSession.objects.get(
                    id=academic_session[0].id)
                dict['grade'] = acad_session.grade.name
                dict['section'] = acad_session.section.name
                activity_missed = GroupActivityMissed.objects.filter(
                    period=class_period.id).count()
                dict['activity_behind'] = activity_missed
                periods_lists.append(dict)
                dict = {}
            context = {"message": "Class List",
                       "data": periods_lists, "statusCode": status.HTTP_200_OK}
            return Response(context)

            # data_dict = {
            #     "teacher": request.data.get('teacher', None)
            # }
            # context = super().get_serializer_context()
            # context.update({"data_dict": data_dict})
            # class_teacher_serializer = ClassAccordingToTeacherSerializer(
            #     data=request.data, context=context,)
            # if class_teacher_serializer.is_valid():
            #     class_teacher_serializer.save()
            #     print("@@@@@@@", class_teacher_serializer.data)
            #     return Response(class_teacher_serializer.data)
            # else:
            #     print(class_teacher_serializer.errors)
            #     return Response(class_teacher_serializer.errors)

        except Exception as ex:
            print("Error view", ex)
            print("Traceback", traceback.print_exc())
            return Response(ex)
