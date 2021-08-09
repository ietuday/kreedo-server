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

""" 
    Packages for uploading csv
"""
import pandas as pd
import math as m
import json
import csv
import traceback
from kreedo.conf import logger
from rest_framework.response import Response
from users.api.custum_storage import FileStorage
from kreedo.conf.logger import CustomFormatter
import logging
from rest_framework import status
import ast

# Create your views here.


""" Logger Function """

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")


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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
   
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



""" Upload Package """
class AddPackage(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_package = []

            for i, f in enumerate(df, start=1):
                f['materials']= ast.literal_eval(f['materials'])
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    package_qs = Package.objects.filter(id=f['id'])[0]
                    package_qs.name = f['name']
                    package_qs.materials = f['materials']
                    package_qs.is_active = f['is_active']
                    package_qs.save()
                    added_package.append(package_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    package_qs = Package.objects.filter(id=f['id'])[0]
                    added_package.append(package_qs)
                    package_qs.delete()
                else:
                    print("Create", f)
                    
                    package_serializer = PackageCreateSerializer(
                        data=dict(f))
                    if package_serializer.is_valid():
                        package_serializer.save()
                        added_package.append(
                            package_serializer.data)
                        print(package_serializer.data)
                    else:
                        
                        raise ValidationError(package_serializer.errors)

            keys = added_package[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_package)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            context = {
                "isSuccess": True, "message": "Package added successfully", "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)
            # return Response(path_to_file)

        except Exception as ex:
            print(ex)
            logger.debug(ex)
            context = {
                "isSuccess": False, "message": "Issue on Package ", "error": "", "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # return Response(ex)


