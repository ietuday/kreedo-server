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
                    print("@@@@@@@@@@", content_type.upper())
                    print("$$$$$$$$$$$$$$", word.upper())
                    model_name = word
                    
            print("model_name-----------", model_name)
            if "Role" == model_name:
                from users.models import Role
                ct = ContentType.objects.get_for_model(Role)
                resultant = permission_creation(ct.id, request.data)
                context = {
                "success": True, "message": "Permission Created", "error": "", "data": resultant}
                return Response(context, status=status.HTTP_200_OK)

            else:
                print("RRRRR")


        except Exception as ex:
            print("ERROR", ex)
            return Response(ex)


""" Permission update ,retrive and delete """


class PermissionRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Permission
    serializer_class = PermissionSerializer
