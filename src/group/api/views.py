import re
from django.apps import apps
from django.shortcuts import render
from django.contrib.auth.models import Group, Permission
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework import status

from django.contrib.contenttypes.models import ContentType

from .serializer import*
from .utils import*
from kreedo.general_views import*
from users.models import *

# Create your views here.

""" Group List and Create """


class GroupListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Group
    serializer_class = GroupSerializer


""" Group update ,retrive and delete """


class GroupRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Group
    serializer_class = GroupSerializer


# from django.db.models import get_app, get_models


""" Permission List and Create """


class PermissionListCreate(ListCreateAPIView):
    model = Permission
    serializer_class = PermissionSerializer

    def post(self, request):

        try:
            content_type = request.data.get('content_type', None)

            app_model_name = [model.__name__ for model in apps.get_models()]
            print("App", app_model_name)

            for word in app_model_name:
                if content_type.upper() == word.upper():
                    model_name = word
                    
            if "Role" == model_name:
                from users.models import Role
                ct = ContentType.objects.get_for_model(Role)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)

            elif "UserType" == model_name:
                from users.models import UserType
                ct = ContentType.objects.get_for_model(UserType)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "UserDetail" == model_name:
                from users.models import UserDetail
                ct = ContentType.objects.get_for_model(UserDetail)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "ReportingTo" == model_name:
                from users.models import ReportingTo
                ct = ContentType.objects.get_for_model(ReportingTo)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "UserRole" == model_name:
                from users.models import UserRole
                ct = ContentType.objects.get_for_model(UserRole)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "SchoolSession" == model_name:
                from session.models import SchoolSession
                ct = ContentType.objects.get_for_model(SchoolSession)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "SchoolCalendar" == model_name:
                from session.models import SchoolCalendar
                ct = ContentType.objects.get_for_model(SchoolCalendar)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "AcademicCalender" == model_name:
                from session.models import AcademicCalender
                ct = ContentType.objects.get_for_model(AcademicCalender)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "AcademicSession" == model_name:
                from session.models import AcademicSession
                ct = ContentType.objects.get_for_model(AcademicSession)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "Grade" == model_name:
                from schools.models import Grade
                ct = ContentType.objects.get_for_model(Grade)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "Section" == model_name:
                from schools.models import Section
                ct = ContentType.objects.get_for_model(Section)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "Subject" == model_name:
                from schools.models import Subject
                ct = ContentType.objects.get_for_model(Subject)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "License" == model_name:
                from schools.models import License
                ct = ContentType.objects.get_for_model(License)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "School" == model_name:
                from schools.models import School
                ct = ContentType.objects.get_for_model(School)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "Room" == model_name:
                from schools.models import Room
                ct = ContentType.objects.get_for_model(Room)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "Plan" == model_name:
                from plan.models import Plan
                ct = ContentType.objects.get_for_model(Plan)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "PeriodTemplate" == model_name:
                from period.models import PeriodTemplate
                ct = ContentType.objects.get_for_model(PeriodTemplate)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "PeriodTemplateDetail" == model_name:
                from period.models import PeriodTemplateDetail
                ct = ContentType.objects.get_for_model(PeriodTemplateDetail)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "Period" == model_name:
                from period.models import Period
                ct = ContentType.objects.get_for_model(Period)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            elif "Package" == model_name:
                from package.models import Package
                ct = ContentType.objects.get_for_model(Package)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)
            
            
            



        except Exception as ex:
            print("ERROR", ex)
            return Response(ex)


""" Permission update ,retrive and delete """


class PermissionRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Permission
    serializer_class = PermissionSerializer
