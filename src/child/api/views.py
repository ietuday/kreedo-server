import traceback
from django.shortcuts import render
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from kreedo.general_views import*
from child.models import*
from .filters import*
from .serializer import*

# Create your views here.

""" create and List Child """


class ChildListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Child
    # filterset_class = ChildFilter


""" Attendance List and Create """


class AttendanceListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Attendance
    # filterset_class = AttendanceFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AttendanceListSerializer

        if self.request.method == 'POST':
            return AttendanceCreateSerializer



""" Attendance Retrive Update and Delete """

class AttendanceRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Attendance

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AttendanceListSerializer

        if self.request.method == 'PUT':
            return AttendanceCreateSerializer

        if self.request.method == 'DELETE':
            return AttendanceListSerializer

