from django.shortcuts import render
from .serializer import*
from .filters import*
from kreedo.general_views import*
from activity.models import*

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

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
        if self.request.method == 'POST':
            return GroupActivityMissedCreateSerilaizer


""" GroupActivityMissed Retrive update Delete """


class GroupActivityMissedRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = GroupActivityMissed
    filterset_class = GroupActivityMissedFilter
    serializer_class = GroupActivityMissedListSerilaizer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupActivityMissedListSerilaizer
        if self.request.method == 'PUT':
            return GroupActivityMissedCreateSerilaizer
