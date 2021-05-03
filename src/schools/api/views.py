from address.api.serializer import AddressSerializer
from .filters import*
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

""" Grade List and Create """
# @permission_classes((IsAuthenticatedOrReadOnly,))


class GradeListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Grade
    serializer_class = GradeSerializer
    filterset_class = GradeFilter


""" Grade Retrive Update Delete """


class GradeRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Grade
    serializer_class = GradeSerializer
    filterset_class = GradeFilter


""" Section List and Create """


class SectionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Section
    filterset_class = SectionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionListSerializer
        if self.request.method == 'POST':
            return SectionListSerializer


""" Section Retrive Update delete """


class SectionRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Section
    filterset_class = SectionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionListSerializer
        if self.request.method == 'PUT':
            return SectionListSerializer
        if self.request.method == 'DELETE':
            return SectionListSerializer


""" Subject List and Create """


class SubjectListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Subject
    filterset_class = SubjectFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectListSerializer
        if self.request.method == 'POST':
            return SubjectCreateSerializer


""" Subject update Retrive and Delete """


class SubjectRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Subject
    serializer_class = SubjectListSerializer
    filterset_class = SubjectFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectListSerializer
        if self.request.method == 'PUT':
            return SubjectCreateSerializer


""" License List and Create """


class LicenseListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = License
    filterset_class = LicenseFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LicenseListSerializer
        if self.request.method == 'POST':
            return LicenseCreateSerializer


""" License update Retrive and Delete """


class LicenseRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = License
    serializer_class = LicenseCreateSerializer
    filterset_class = LicenseFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LicenseListSerializer
        if self.request.method == 'PUT':
            return LicenseCreateSerializer


""" School List and Create """


class SchoolListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = School
    # serializer_class = SchoolSerializer
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolListSerializer
        if self.request.method == 'POST':
            return SchoolCreateSerializer

    def post(self, request):
        address_detail = {
            "country": request.data.get('country', None),
            "state": request.data.get('state', None),
            "city": request.data.get('city', None),
            "address": request.data.get('address', None),
            "pincode": request.data.get('pincode', None),
        }
        address_serializer = AddressSerializer(data=address_detail)
        if address_serializer.is_valid():
            address_serializer.save()
        else:
            raise serializers.ValidationError(
                "address_serializer._errors", address_serializer._errors)
        school_data = {
            "name": request.data.get('name', None),
            "type": request.data.get('type', None),
            "logo": request.data.get('logo', None),
            "address": address_serializer.data['id'],
            "license": request.data.get('license', None),
            "is_active": request.data.get('is_active', None),
        }

        context = self.get_serializer_context()
        context.update({"school_data": school_data})

        school_serializer = SchoolCreateSerializer(
            data=dict(school_data), context=context)
        if school_serializer.is_valid():
            school_serializer.save()
            return Response(school_serializer.data)
        return Response(school_serializer.errors)


""" School update Retrive and Delete """


class SchoolRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = School
    serializer_class = SchoolListSerializer
    filterset_class = SchoolFilter


""" Section Subject Teacher List and Create """


class SectionSubjectTeacherListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SectionSubjectTeacher

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionSubjectTeacherListSerializer
        if self.request.method == 'POST':
            return SectionSubjectTeacherCreateSerializer


"""Section Subject Teacher  update Retrive and Delete """


class SectionSubjectTeacherRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SectionSubjectTeacher
    serializer_class = SectionSubjectTeacherCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionSubjectTeacherListSerializer
        if self.request.method == 'PUT':
            return SectionSubjectTeacherCreateSerializer


""" Room List and Create """


class RoomListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Room
    filterset_class = RoomFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoomListSerializer
        if self.request.method == 'POST':
            return RoomCreateSerializer


""" Room update and Retrive """


class RoomRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Room
    filterset_class = RoomFilter
    # serializer_class = RoomListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoomListSerializer
        if self.request.method == 'PUT':
            return RoomCreateSerializer
        if self.request.method == 'DELETE':
            return RoomListSerializer
