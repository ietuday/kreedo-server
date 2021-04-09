from django.shortcuts import render

from .serializer import*
from holiday.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from .filters import*
# Create your views here.

""" School Holiday List and create """


class SchoolHolidayListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolHoliday
    filterset_class = SchoolHolidayFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolHolidayListSerializer
        if self.request.method == 'POST':
            return SchoolHolidayCreateSerializer


""" School Holiday Reetrive Update delete """


class SchoolHolidayRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SchoolHoliday
    serializer_class = SchoolHolidayCreateSerializer
    filterset_class = SchoolHolidayFilter
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolHolidayListSerializer
        if self.request.method == 'PUT':
            return SSchoolHolidayCreateSerializer


""" School Weak off List and create """


class SchoolWeakOffListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolWeakOff
    filterset_class = SchoolWeakOffFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolWeakOffListSerializer
        if self.request.method == 'POST':
            return SchoolWeakOffCreateSerializer


""" School Weak off Retrive Update Delte """


class SchoolWeakOffRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateAPIView):
    model = SchoolWeakOff
    filterset_class = SchoolWeakOffFilter
    serializer_class = SchoolWeakOffCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolWeakOffListSerializer
        if self.request.method == 'PUT':
            return SchoolWeakOffCreateSerializer

""" Create Calendar """
class Calendar(CreateAPIView):
    def post(self,request):
        pass
