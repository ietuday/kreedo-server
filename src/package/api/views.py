# from .filters import*
from .serializer import*
from package.models import*
from kreedo.general_views import*
from django.shortcuts import render

"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


from .filters import *
# Create your views here.


""" Package List and Create """


class PackageListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Package

    # filterset_class = PackageFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PackageListSerializer
        if self.request.method == 'POST':
            return PackageCreateSerializer


""" Package Retrive Update Delete """


class PackageRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Package
    serializer_class = PackageListSerializer
    # filterset_class = PackageFsilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PackageListSerializer
        if self.request.method == 'PUT':
            return PackageCreateSerializer


""" School Package List and Create """


class SchoolPackageListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolPackage
    filterset_class = SchoolPackageFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolPackageListSerializer
        if self.request.method == 'POST':
            return SchoolPackageCreateSerializer


""" school package Retreive update and delete """


class SchoolPackageRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SchoolPackage
    filterset_class = SchoolPackageFilter
    serializer_class = SchoolPackageListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolPackageListSerializer
        if self.request.method == 'PUT':
            return SchoolPackageCreateSerializer
