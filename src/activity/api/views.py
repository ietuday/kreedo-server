from django.shortcuts import render
from .serializer import*
from .filters import*
from kreedo.general_views import*
from activity.models import*

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
# Create your views here.

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
            data = request.data

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
            return Response(ex)
