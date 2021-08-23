from pdb import set_trace
from period.models import Period
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import render
from .serializer import*
from .filters import*
from kreedo.general_views import*
from activity.models import*
from users.models import*

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

""" 
    Packages for uploading csv
"""
import pandas as pd
import math as m
import json
import csv
import traceback
from kreedo.conf import logger
from rest_framework.response import Response
from users.api.custum_storage import FileStorage
from kreedo.conf.logger import CustomFormatter
import logging
from rest_framework import status
import ast
from rest_framework.pagination import LimitOffsetPagination


# Create your views here.


""" Logger Function """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")

""" Activity List And create """


class ActivityListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Activity
    filterset_class = ActivityFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityListSerializer
        if self.request.method == 'POST':
            return ActivityCreateSerializer


class ActivityListBySubject(GeneralClass, Mixins,  ListAPIView):
    model = Activity
    filterset_class = ActivityFilter
    # pagination_class = LimitOffsetPagination
    serializer_class = ActivityListSerializer

    def get(self, request, *args, **kwargs):
        try:

            subject = kwargs.get('subject', None)
            child = kwargs.get('child', None)
            context = self.get_serializer_context()
            context['child'] = child
            activity_list = Activity.objects.filter(subject=subject)
            print('list', activity_list)
            page = self.paginate_queryset(activity_list)
            if page is not None:
                serializer = self.get_serializer(
                    page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            activity_serializer = ActivityListSerializer(
                activity_list, many=True, context=context)
            return Response(activity_serializer.data)

        except Exception as ex:
            print(ex)
            return Response(ex)


"activity list by subject for web"
class ActivityListBySubjectWeb(GeneralClass, Mixins,  ListAPIView):
    model = Activity
    filterset_class = ActivityFilter
    # pagination_class = LimitOffsetPagination
    serializer_class = ActivityListWebSerializer

""" Activity Retrive Update and delete"""
class ActivityRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Activity
    filterset_class = ActivityFilter
    serializer_class = ActivityListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityListSerializer
        if self.request.method == 'PUT':
            return ActivityUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Activity Asset List And create """


class ActivityAssetListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = ActivityAsset
    filterset_class = ActivityAssetFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityAssetListSerializer
        if self.request.method == 'POST':
            return ActivityAssetCreateSerializer


""" ActivityAsset Retrive Update and delete"""


class ActivityAssetRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = ActivityAsset
    filterset_class = ActivityAssetFilter
    serializer_class = ActivityAssetListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityAssetListSerializer
        if self.request.method == 'PUT':
            return ActivityAssetUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Activity  CompleteList and Create """


class ActivityCompleteListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = ActivityComplete
    filterset_class = ActivityCompleteFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityCompleteListSerilaizer

    def post(self, request):
        try:
            print(request.data.get('activity_complete', None))
            activity_complete_serializer = ActivityCompleteCreateSerilaizer(
                data=request.data.get('activity_complete', None), many=True)
            if activity_complete_serializer.is_valid():
                activity_complete_serializer.save()
                return Response(activity_complete_serializer.data)
            else:
                return Response(activity_complete_serializer.errors)
        except Exception as ex:
            return Response(ex)


class ActivityCompleteListCreateMob(GeneralClass, Mixins, ListCreateAPIView):
    model = ActivityComplete

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityCompleteListSerilaizer

    def post(self, request):
        activity_complete_list = request.data.get('activity_complete', None)
        activity_complete_data = []
        for activity in activity_complete_list:
            record_aval = ActivityComplete.objects.filter(
                child=activity.get('child'),
                activity=activity.get('activity')
            ) 
            

            if activity['is_completed'] == False:
                period = Period.objects.get(pk=activity['period'])
                next_period = Period.objects.filter(
                                period_template_detail=period.period_template_detail,
                                subject=period.subject,
                                id__gt=period.id).order_by('id').first()
                print("next period",next_period)
                if next_period:
                    activity['activity_reschedule_period'] = next_period.id
                else:
                    activity['activity_reschedule_period'] = None
            else:
                activity['activity_reschedule_period'] = None

            if record_aval:
                activity_complete_serializer = ActivityCompleteCreateSerilaizer(
                    record_aval[0], data=activity)
            else:
                activity_complete_serializer = ActivityCompleteCreateSerilaizer(
                    data=activity)
            if activity_complete_serializer.is_valid():
                activity_complete_serializer.save()
                activity_complete_data.append(
                    activity_complete_serializer.data)
                

                if activity['is_completed'] == True and (activity['behind_activity'] == True or activity['behind_activity'] == False) :
                    chk_activity_complete = ActivityComplete.objects.filter(
                                                            activity=activity['activity'],
                                                            period=activity['period']
                                                        ).exclude(
                                                            is_completed=True
                                                        )

                    # pdb.set_trace()                                 
                    if len(chk_activity_complete) == 0:
                        period_b = Period.objects.get(pk=activity['period'])
                        activity_b = Activity.objects.get(pk=activity['activity'])
                        # pdb.set_trace()
                        period_b.activity_done.add(activity_b)
                        period_b.save()
                        # pdb.set_trace()
                continue
            return Response(activity_complete_serializer.errors)
            

        return Response(activity_complete_data)





""" Activity complete list create for group activtity completion"""

class ActivityCompleteListCreateGroup(GeneralClass, Mixins, ListCreateAPIView):
    model = ActivityComplete

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityCompleteListSerilaizer

    def post(self, request):
        try:
            activity_complete_data = request.data.get(
                'activity_complete', None)
            activity_updated_data = []

            for activity in activity_complete_data:
                activity_q = ActivityComplete.objects.filter(
                    child=activity.get('child'),
                    activity=activity.get('activity')
                      )

                if activity_q:
                    activity_complete = ActivityCompleteCreateSerilaizer(
                        activity_q[0], data=activity)
                else:
                    activity_complete = ActivityCompleteCreateSerilaizer(
                        data=activity)

                if activity_complete.is_valid():
                    activity_complete.save()
                    activity_updated_data.append(activity_complete.data)
                    continue
                return Response(activity_complete.errors)
            return Response(activity_updated_data)

        except Exception as ex:
            print("error", ex)
            return Response(ex)


""" ActivityComplete Retrive update Delete """

class ActivityCompleteRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = ActivityComplete
    filterset_class = ActivityCompleteFilter
    serializer_class = ActivityCompleteListSerilaizer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityCompleteListSerilaizer

    def put(self, request, *args, **kwargs):
        try:

            serializer = ActivityCompleteCreateSerilaizer(
                data=request.data.get('activity_complete', None), many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
            return Response(serializer.data)
        except Exception as ex:
            return Response(ex)


""" Upload Activity """


class AddActivity(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_activity = []

            for i, f in enumerate(df, start=1):
                f['master_material'] = ast.literal_eval(f['master_material'])
                f['supporting_material'] = ast.literal_eval(
                    f['supporting_material'])
                f['subject'] = ast.literal_eval(f['subject'])
                if not m.isnan(f['id']) and f['is_Deleted'] == False:
                    print("UPDATION")
                    activity_qs = Activity.objects.filter(id=f['id'])[0]

                    activity_qs.name = f['name']
                    activity_qs.type = f['type']
                    activity_qs.objective = f['objective']
                    activity_qs.description = f['description']
                    activity_qs.master_material.set(f['master_material'])
                    activity_qs.subject.set(f['subject'])
                    activity_qs.supporting_material.set(
                        f['supporting_material'])
                    activity_qs.is_active = f['is_active']
                    activity_qs.created_by = UserDetail.objects.filter(
                        user_obj=f['created_by'])[0]
                    activity_qs.save()
                    activity_serializer = ActivityCreateSerializer(activity_qs)
                    added_activity.append(activity_serializer.data)
                elif not m.isnan(f['id']) and f['is_Deleted'] == True:
                    print("DELETION")
                    activity_qs = Activity.objects.filter(id=f['id'])[0]
                    activity_serializer = ActivityCreateSerializer(activity_qs)
                    added_activity.append(activity_serializer.data)
                    # added_activity.append(activity_qs)
                    activity_qs.delete()
                else:
                    print("Create")
                    activity_detail = {
                        "name": f.get('name', None),
                        "type": f.get('type', None),
                        "objective": f.get('objective', None),
                        "description": f.get('description', None),
                        "master_material": f.get('master_material', None),
                        "supporting_material": f.get('supporting_material', None),
                        "subject": f.get('subject', None),
                        "is_active": f.get('is_active', None),
                        "created_by": f.get('created_by', None)
                    }
                    print(activity_detail)
                    print(f)

                    activity_serializer = ActivityCreateSerializer(
                        data=dict(activity_detail))
                    if activity_serializer.is_valid():
                        activity_serializer.save()
                        added_activity.append(
                            activity_serializer.data)
                        print(activity_serializer.data)
                    else:
                        raise ValidationError(activity_serializer.errors)
            print(added_activity[0])
            print(added_activity[0].keys())
            keys = added_activity[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_activity)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            context = {"isSuccess": True, "message": "Activity Added sucessfully",
                       "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)
            # return Response(path_to_file, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            logger.debug(ex)
            print(traceback.print_exc())
            context = {"isSuccess": False, "message": "Issue Activity",
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddActivityAsset(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_activity = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    activity_qs = ActivityAsset.objects.filter(id=f['id'])[0]
                    activity_qs.activity = f['activity']
                    activity_qs.type = f['type']
                    activity_qs.activity_data = f['activity_data']
                    activity_qs.title = f['title']
                    activity_qs.description = f['description']
                    activity_qs.is_active = f['is_active']
                    activity_qs.save()
                    added_activity.append(activity_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    activity_qs = ActivityAsset.objects.filter(id=f['id'])[0]
                    added_activity.append(activity_qs)
                    activity_qs.delete()
                else:
                    print("Create")
                    activity_detail = {
                        "activity": f.get('activity', None),
                        "type": f.get('type', None),
                        "activity_data": f.get('activity_data', None),
                        "title": f.get('title', None),
                        "description": f.get('description', None),
                        "is_active": f.get('is_active', None),
                        "created_by": f.get('created_by', None)
                    }
                    print(activity_detail)
                    print(f)

                    activity_serializer = ActivityAssetCreateSerializer(
                        data=dict(activity_detail))
                    if activity_serializer.is_valid():
                        activity_serializer.save()
                        added_activity.append(
                            activity_serializer.data)
                        print(activity_serializer.data)
                    else:
                        raise ValidationError(activity_serializer.errors)

            keys = added_activity[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_activity)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            context = {"isSuccess": True, "message": "Activity Asset Added sucessfully",
                       "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)
            # return Response(path_to_file, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            logger.debug(ex)
            context = {"isSuccess": False, "message": "Issue Activity Asset",
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
