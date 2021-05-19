from django.shortcuts import render
from django.contrib.auth.models import Group,Permission
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from django.contrib.contenttypes.models import ContentType

from .serializer import*
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
from django.apps import apps


""" Permission List and Create """
class PermissionListCreate(ListCreateAPIView):
    model = Permission
    serializer_class = PermissionSerializer

    def post(self,request):

        try:
            content_type = request.data.get('content_type',None)
            print("@@@@@@@@@@@@@@@@",content_type)

            model_name = [model.__name__ for model in apps.get_models()]
            print("App", model_name)
            for name in model_name:
                if content_type.upper() in name.upper():
                    print("Model------>", content_type)


            # for model in get_models(apps):
            #     # do something with the model
            #     print("Modal", Modal)

            # ct = ContentType.objects.get_for_model(Role)
            # print("Contentv Type", ct.id)



            # permission_data = {
            #     "name":request.data.get('name', None),
            #     "content_type":ct.id,
            #     "codename":request.data.get('codename',None)

            # }
            # permission_serializer = PermissionSerializer(data=dict(permission_data))
            # if permission_serializer.is_valid():
            #     permission_serializer.save()
            #     return Response(permission_serializer.data)
            # else:
            #     print(permission_serializer.errors)
            #     return Response(permission_serializer.errors)

        except Exception as ex:
            print("ERROR", ex)
            return Response(ex)



""" Permission update ,retrive and delete """
class PermissionRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Permission
    serializer_class = PermissionSerializer




