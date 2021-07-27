from django.shortcuts import render
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
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
from activity.api.serializer import*

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


""" Period Retrive and Update"""


class PeriodRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Period
    filterset_class = PeriodFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PeriodListSerializer
        if self.request.method == 'PUT':
            return PeriodCreateSerializer
        if self.request.method == 'PATCH':
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
        if self.request.method == 'PATCH':
            return PeriodTemplateDetailCreateSerializer
        



""" List of classes acording to teacher id , date, and day """


class ClassAccordingToTeacher(GeneralClass, Mixins, ListCreateAPIView):
    # model = Period
    # serializer_class = ClassAccordingToTeacherSerializer

    def post(self, request):

        try:

            teacher = request.data.get('teacher', None)
            period_list_qs = Period.objects.filter(
                teacher=teacher, start_date = request.data.get('start_date'))

            if len(period_list_qs) !=0:
                periods_lists = []
                dict = {}
                for class_period in period_list_qs:
                    dict['period_id'] = class_period.id
                    dict['name'] = class_period.name
                    dict['description'] = class_period.description
                    dict['room_no'] = class_period.room_no.room_no
                    dict['start_time'] = class_period.start_time.strftime(
                        "%H:%M:%S")
                    dict['end_time'] = class_period.end_time.strftime("%H:%M:%S")
                    dict['is_complete'] = class_period.is_complete
                    dict['is_active'] = class_period.is_active
                    dict['type'] = class_period.type
                    academic_session = class_period.academic_session.all()
               
                    dict['academic_session'] = academic_session[0].id
                    acad_session = AcademicSession.objects.get(
                        id=academic_session[0].id)
                    dict['grade'] = acad_session.grade.name
                    dict['grade_id'] = acad_session.grade.id
                    dict['section'] = acad_session.section.name
                    dict['section_id'] = acad_session.section.id
                    dict['subject'] = class_period.subject.name
                    dict['subject_id'] = class_period.subject.id

                    activity_list = class_period.subject.activity.all()
                    activitys_list = []
                    activitys_dict = {}
                    for activity_obj in activity_list:
                        activity_obj_id = Activity.objects.filter(
                            id=activity_obj.id)
                        for active in activity_obj_id:
                            activitys_dict['type'] = active.type
                            activitys_list.append(activitys_dict)

                    dict['activity_type'] = activitys_dict.get('type')
                    activity_missed = ActivityComplete.objects.filter(
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
                                master_material_dict['description'] = m.description
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
                                supporting_master_material_dict['description'] = m.description
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
                return Response(periods_lists, status=status.HTTP_200_OK)
            else:
                return Response("Period list not found",status=status.HTTP_404_NOT_FOUND )

        except Exception as ex:
            logger.debug(ex)
            logger.info(ex)
            # context = {"error": ex, 'isSuccess': False,
            #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Activity according to child """


class ActivityByChild(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            child = request.data.get('child', None)
            period = request.data.get('period', None)
            grade = request.data.get('grade', None)
            section = request.data.get('section', None)

            activity_missed_qs = ActivityComplete.objects.filter(child__id=child,
                                                                 period=period)
            activity_missed_serializer = ActivityCompleteSerilaizer(
                activity_missed_qs, many=True)

            # context = {"message": "Activity List by Child",
            #            "data": activity_missed_serializer.data, "statusCode": status.HTTP_200_OK}
            return Response(activity_missed_serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            # context = {"error": ex, 'isSuccess': False,
            #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityListByChild(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            child = request.data.get('child', None)
            period = request.data.get('period', None)

            activity_missed_qs = ActivityComplete.objects.filter(child=child,
                                                                 period=period)

            if len(activity_missed_qs) !=0:                                                    
                activity_missed_serializer = ActivityCompleteListChildSerilaizer(
                    activity_missed_qs, many=True)
                return Response(activity_missed_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Activity Complete list by child is not found",status=status.HTTP_404_NOT_FOUND )
        except Exception as ex:
         
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityDetail(GeneralClass, Mixins, RetrieveAPIView):
    model = Activity
    serializer_class = ActivitySerializer


""" Apply Period template to academic session """


class PeriodTemplateAppyToGradesListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = PeriodTemplateToGrade
    filterset_class = PeriodTemplateToGradeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PeriodTemplateToGradeListSerializer

    def post(self, request):
        try:

            grade_list = request.data.get('grade_list')
            print(grade_list)
            for grade in grade_list:
            
                academic_qs = AcademicSession.objects.filter(grade=grade['grade'], section=grade['section'], school_calender=grade['academic_calender'])[0]
         
                grade['academic_session']=academic_qs.id

            period_template_to_grade_serializer = PeriodTemplateToGradeCreateSerializer(
                data=request.data.get('grade_list'),many=True)

            if period_template_to_grade_serializer.is_valid():
                period_template_to_grade_serializer.save()
                return Response(period_template_to_grade_serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(period_template_to_grade_serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PeriodTemplateAppyToGradesRetriveUpdateDestroy(GeneralClass, Mixins,RetrieveUpdateDestroyAPIView):
    model = PeriodTemplateToGrade
    filterset_class = PeriodTemplateToGradeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PeriodTemplateToGradeListSerializer
        if self.request.method == 'PUT':
            return PeriodTemplateToGradeCreateSerializer
        if self.request.method == 'PATCH':
            return PeriodTemplateToGradeCreateSerializer
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)





""" Period List and Create """


class PeriodListCreate(GeneralClass, Mixins, ListCreateAPIView):
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
                return Response(working_days,status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERRROR", ex)
            logger.info(ex)
            context = {"error": ex, 'isSuccess': False,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(context)


""" Period Create """


class PeriodCreate(GeneralClass, Mixins, ListCreateAPIView):
    # model = Period
    # filterset_class = PeriodFilter

    def post(self, request):
        try:

            grade_dict = {
                "grade": request.data.get('grade', None),
                "section": request.data.get('section', None),
                "start_date": request.data.get('start_date', None),
                "end_date": request.data.get('end_date', None),
                "acad_session": request.data.get('acad_session', None)
            }

            """ Get Holidays Function Call """
            school_holiday_count = school_holiday(grade_dict)
            print("COUNT----------->", school_holiday_count)
            """ Get Weak-off Function Call """
            week_off = weakoff_list(grade_dict)
            print("week_off-------->", week_off)
            """ Weekday Count """
            count_weekday = weekday_count(grade_dict, week_off)
            print("count_weekday----->", count_weekday)
            """ Count Working Days """
            working_days = total_working_days(grade_dict, count_weekday)
            print("working_days---->", working_days)
            """ Period Creation """
            period_reponse = create_period(grade_dict)
            print("period Response------->", period_reponse)
            return Response(period_reponse,status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERRROR", ex)
            logger.info(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" MONTH LIST """
class PeriodMonthList(GeneralClass,Mixins,ListCreateAPIView):
    def post(self, request):
        try:

            academic_id = AcademicSession.objects.get(
                grade=request.data.get('grade',None), section=request.data.get('section',None)).id
            period_qs= Period.objects.filter(start_date__year=request.data.get('year',None),
                           start_date__month=request.data.get('month',None))
            period_list = []
            
            for i in period_qs:
                period_dict = {}
                period_count=Period.objects.filter(start_date=i.start_date)
                for j in period_count:
                    print("%%%%%%%%%%%%%%%----->", j.start_date)
                dates =i.start_date
                period_dict['start_date']  = j.start_date.strftime("%Y/%m/%d")
                period_dict['period_count'] = period_count.count()
                if SchoolHoliday.objects.filter(holiday_from=j.start_date,academic_session=academic_id).exists():
                    is_holiday = "true"
                else:
                    is_holiday ="false"
                day_name = j.start_date.strftime('%A')
              
                period_dict['is_holiday'] =is_holiday
                period_list.append(period_dict)
                period_dict = {}

            return Response(period_list,status=status.HTTP_200_OK)
        
        except Exception as ex:
            print("ERROR------->", ex)

            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         

"""  Date according period list """
class PerioListAccordingDate(GeneralClass,Mixins,ListCreateAPIView):
    def post(self,request):
        try:
            period_qs = Period.objects.filter(academic_session=request.data.get('academic_session', None),start_date=request.data.get('start_date',None))
   
            period_serializer = PeriodListSerializer(period_qs,many=True)
            return Response(period_serializer.data,status=status.HTTP_200_OK)     
        except Exception as ex:
          
            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         

""" Period Template Detail List By  Period Template by  ID """
class PeriodTemplateDetailByPeriodTemplate(GeneralClass, Mixins,ListCreateAPIView):
    def get(self,request,pk):
        try:
            period_template = PeriodTemplate.objects.filter(id=pk)
            period_template_serializer = PeriodTemplateListSerializer(period_template,many=True)
            return Response(period_template_serializer.data,status=status.HTTP_200_OK)
            
        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Period Count According Date Month List """
class PeriodCountListByAcademicSession(GeneralClass,Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            period_data = Period.objects.filter(start_date__year=request.data.get('year',None),
                           start_date__month=request.data.get('month',None),academic_session=request.data.get('academic_session',None))
            print("period_data--------------->", period_data)
            period_list = []
            
            for period_qs in period_data:
                print(period_qs)
                period_dict = {}
                period_count=Period.objects.filter(start_date=period_qs.start_date)
                period_dict['period_count'] =period_count.count()
                for period in period_count:
                
                    period_dict['start_date']  = period.start_date.strftime("%Y/%m/%d")
               
                    if SchoolHoliday.objects.filter(holiday_from=period.start_date,academic_session=request.data.get('academic_session',None)).exists():
                        is_holiday = "true"
                    else:
                        is_holiday ="false"
                    day_name = period.start_date.strftime('%A')
              
                period_dict['is_holiday'] =is_holiday
                period_list.append(period_dict)
                period_dict = {}

            return Response(period_list,status=status.HTTP_200_OK)

            

        except Exception as ex:
            print("ERROR", ex)
            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
