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


""" GroupActivityMissed List and Create """


class GroupActivityMissedListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = GroupActivityMissed
    filterset_class = GroupActivityMissedFilter
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupActivityMissedListSerilaizer

    def post(self, request):
        try:
            group_activity_serializer = GroupActivityMissedCreateSerilaizer(data=request.data,
                            many=True)
            if group_activity_serializer.is_valid():
                group_activity_serializer.save()
                return Response(group_activity_serializer.data)
            else:
                return Response(group_activity_serializer.errors)
        except Exception as ex:
            return Response(ex)


""" GroupActivityMissed Retrive update Delete """


class GroupActivityMissedRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = GroupActivityMissed
    filterset_class = GroupActivityMissedFilter
    serializer_class = GroupActivityMissedListSerilaizer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupActivityMissedListSerilaizer
       
    
    def put(self, request, *args, **kwargs):
        data = request.data
        print("data", data)
        group_ids = [i['id'] for i in data]
        print("###", group_ids)
        self.validate_ids(group_ids)
        
        instances = []
        for temp_dict in data:
            id = temp_dict['id']
            child = temp_dict['child']
            period = temp_dict['period']
            activity = temp_dict['activity']
            is_completed = temp_dict['is_completed']
            is_active = temp_dict['is_active']
            obj = GroupActivityMissed.objects.get(pk=id)
            print("%%%%%%%", obj)
            obj.child = child
            obj.period = period
            obj.activity = activity
            obj.is_active = is_active
            obj.save()
            instances.append(obj)
        serializer = GroupActivityMissedCreateSerilaizer(instances, many=True)
        return Response(serializer.data)
            