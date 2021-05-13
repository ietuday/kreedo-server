from django.shortcuts import render
from .serializer import*
from .filters import*
from kreedo.general_views import*
from activity.models import*

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
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


""" Activity Retrive Update and delete"""


class ActivityRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Activity
    filterset_class = ActivityFilter
    serializer_class = ActivityListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityListSerializer
        if self.request.method == 'PUT':
            return ActivityCreateSerializer


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
            return ActivityAssetCreateSerializer


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
            activity_complete_serializer = ActivityCompleteCreateSerilaizer(data=request.data.get('activity_complete', None),many=True)
            if activity_complete_serializer.is_valid():
                activity_complete_serializer.save()
                return Response(activity_complete_serializer.data)
            else:
                return Response(activity_complete_serializer.errors)
        except Exception as ex:
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
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    activity_qs = Activity.objects.filter(id=f['id'])[0]
                    activity_qs.name = f['name']
                    activity_qs.type = f['type']
                    activity_qs.objective = f['objective']
                    activity_qs.description = f['description']
                    activity_qs.master_material = f['master_material']
                    activity_qs.subject = f['subject']
                    activity_qs.supporting_material = f['supporting_material']
                    activity_qs.is_active = f['is_active']
                    activity_qs.save()
                    added_activity.append(activity_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    activity_qs = Activity.objects.filter(id=f['id'])[0]
                    added_activity.append(activity_qs)
                    activity_qs.delete()
                else:
                    print("Create")
                    
                    activity_serializer = ActivityCreateSerializer(
                        data=dict(f))
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
                dict_writer.writerows(added_material)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            return Response(path_to_file)

        except Exception as ex:
           
            logger.debug(ex)
            return Response(ex)


