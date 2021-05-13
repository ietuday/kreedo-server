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
            print("",request.data.get('activity_complete', None))
            activity_complete = request.data.get('activity_complete', None)
            print("##############",activity_complete)
            data = activity_complete
            print("@@@", data)

            child_data_ids = [i['id'] for i in data]

            for i in child_data_ids:
                instances = []
                for temp_dict in data:
                    id = temp_dict['id']
                    child = temp_dict['child']
                    period = temp_dict['period']
                    activity = temp_dict['activity']
                    is_completed = temp_dict['is_completed']
                    is_active = temp_dict['is_active']

                    obj = ActivityComplete.objects.get(pk=i)
                    obj.child.id = child
                    obj.period.id = period
                    obj.activity.id = activity
                    obj.is_active = is_active
                    obj.save()
                    instances.append(obj)
                serializer = ActivityCompleteCreateSerilaizer(
                    instances, many=True)
                return Response(serializer.data)
        except Exception as ex:
            print("&&&&&&&&&&&&",ex)
            return Response(ex)


""" Upload Activity """


class AddPackage(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_material = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    package_qs = Package.objects.filter(id=f['id'])[0]
                    package_qs.name = f['name']
                    package_qs.materials = f['materials']
                    package_qs.is_active = f['is_active']
                    package_qs.save()
                    added_package.append(package_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    package_qs = Package.objects.filter(id=f['id'])[0]
                    added_package.append(package_qs)
                    package_qs.delete()
                else:
                    print("Create")
                    
                    package_serializer = PackageCreateSerializer(
                        data=dict(f))
                    if package_serializer.is_valid():
                        package_serializer.save()
                        added_package.append(
                            package_serializer.data)
                        print(package_serializer.data)
                    else:
                        
                        raise ValidationError(package_serializer.errors)

            keys = added_package[0].keys()
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


