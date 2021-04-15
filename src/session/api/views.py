from .filters import *
from .serializer import*
from schools.models import*
from kreedo.general_views import *
from django.shortcuts import render
"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response

"""
    IMPORT CORE FILES 
"""

"""
    IMPORT USER APP FILE
"""
# Create your views here.

""" School Session Create  and list """


class SchoolSessionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolSession
    serializer_class = SchoolSessionSerializer
    filterset_class = SchoolSessionFilter


""" School Session Retrive Update Delete """


class SchoolSessionRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SchoolSession
    serializer_class = SchoolSessionSerializer
    filterset_class = SchoolSessionFilter


""" AcademicSession Create  and list """


class AcademicSessionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = AcademicSession
    # filterset_class = AcademicSessionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcademicSessionListSerializer
        if self.request.method == 'POST':
            return AcademicSessionCreateSerializer


""" AcademicSession Retrive Update Delete """


class AcademicSessionRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = AcademicSession
    serializer_class = AcademicSessionListSerializer
    # filterset_class = AcademicSessionFilter
