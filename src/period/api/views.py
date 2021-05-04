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
from material.models import*
from kreedo.conf.logger import CustomFormatter
import logging
# Create your views here.


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("VIEW CAlled ")

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

            period_list_qs = Period.objects.filter(
                teacher=teacher[0], start_date=request.data.get('start_date'))

            periods_lists = []
            dict = {}
            for class_period in period_list_qs:
                dict['period_id'] = class_period.id
                dict['name'] = class_period.name
                dict['description'] = class_period.description
                dict['room_no'] = class_period.room_no.room_no
                dict['start_time'] = class_period.start_time
                dict['end_time'] = class_period.end_time
                dict['type'] = class_period.type
                academic_session = class_period.academic_session.all()
                acad_session = AcademicSession.objects.get(
                    id=academic_session[0].id)
                dict['grade'] = acad_session.grade.name
                dict['section'] = acad_session.section.name
                dict['subject'] = class_period.subject.name
                activity_list= class_period.subject.activity.all()
                activitys_list = []
                activitys_dict = {}
                for activity_obj in activity_list:
                    activity_obj_id = Activity.objects.filter(id=activity_obj.id)
                    for active in activity_obj_id:
                        activitys_dict['type'] = active.type
                        activitys_list.append(activitys_dict)
                dict['activity_type'] = activitys_list
                activity_missed = GroupActivityMissed.objects.filter(
                    period=class_period.id, is_completed=False)
                dict['activity_behind_count'] = activity_missed.count()
                missed_activity_list = []
                missed_activity_dict = {}
                for miss_activity in activity_missed:
                    missed_activity_dict['id'] = miss_activity.activity.id
                    missed_activity_dict['name'] = miss_activity.activity.name
                    missed_activity_dict['type'] = miss_activity.activity.type
                    missed_activity_dict['objective'] = miss_activity.activity.objective
                    missed_activity_dict['description'] = miss_activity.activity.description
                    activity_asset = ActivityAsset.objects.filter(
                        activity=miss_activity.activity.id)
                    activity_asset_list = []
                    activity_asset_dict = {}
                    for asset in activity_asset:
                        activity_asset_dict['activity_id'] = asset.activity.id
                        activity_asset_dict['type'] = asset.type
                        activity_asset_dict['activity_data'] = asset.activity_data
                        activity_asset_dict['title'] = asset.title
                        activity_asset_dict['description'] = asset.description
                        activity_asset_list.append(activity_asset_dict)

                    master_material = miss_activity.activity.master_material.all()
                    master_material_list = []
                    master_material_dict = {}
                    for material in master_material:
                        material_id = Material.objects.filter(id=material.id)
                        for m in material_id:
                            master_material_dict['name'] = m.name
                            master_material_dict['decription'] = m.decription
                            master_material_dict['photo'] = m.photo
                            master_material_list.append(master_material_dict)
                            master_material_dict = {}

                    missed_activity_dict['master_material'] = master_material_list
                    supporting_material = miss_activity.activity.supporting_material.all()
                    supporting_master_material_list = []
                    supporting_master_material_dict = {}
                    for material in supporting_material:
                        material_id = Material.objects.filter(id=material.id)
                        for m in material_id:
                            supporting_master_material_dict['name'] = m.name
                            supporting_master_material_dict['decription'] = m.decription
                            supporting_master_material_dict['photo'] = m.photo
                            supporting_master_material_list.append(
                                supporting_master_material_dict)
                            supporting_master_material_dict = {}
                    missed_activity_dict['supporting_material'] = supporting_master_material_list
                    missed_activity_dict['activity_asset'] = activity_asset_list
                    missed_activity_list.append(missed_activity_dict)
                    missed_activity_dict = {}
                dict['missed_activity'] = missed_activity_list

                periods_lists.append(dict)
                dict = {}
            context = {"message": "Class List",
                       "data": periods_lists, "statusCode": status.HTTP_200_OK}
            return Response(context)

        except Exception as ex:
            logger.debug(ex)
            logger.info(ex)
            return Response(ex)



