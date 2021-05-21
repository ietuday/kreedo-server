from django.shortcuts import render
from django.shortcuts import render
from .serializer import*
from .filters import*
from kreedo.general_views import*
from material.models import*

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
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


""" List and Create of Material """


class MaterialListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Material
    filterset_class = MaterialFilter
    serializer_class = MaterialSerializer


""" Retrive Update Delete Material """


class MaterialRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Material
    filterset_class = MaterialFilter
    serializer_class = MaterialSerializer


""" Activity Master Supporting Material List and Create  """


class ActivityMasterSupportingMaterialListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = ActivityMasterSupportingMaterial
    filterset_class = ActivityMasterSupportingMaterialFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityMasterSupportingMaterialListSerializer
        if self.request.method == 'POST':
            return ActivityMasterSupportingMaterialCreateSerializer


""" Bulk Upload of Material """


class AddMaterial(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_material = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    material_qs = Material.objects.filter(id=f['id'])[0]
                    material_qs.name = f['name']
                    material_qs.description = f['description']
                    material_qs.photo = f['photo']
                    material_qs.code = f['code']
                    material_qs.is_active = f['is_active']
                    material_qs.save()
                    added_material.append(material_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    material_qs = Material.objects.filter(id=f['id'])[0]
                    added_material.append(material_qs)
                    material_qs.delete()
                else:
                    print("Create")

                    material_serializer = MaterialSerializer(
                        data=dict(f))
                    if material_serializer.is_valid():
                        material_serializer.save()
                        added_material.append(
                            material_serializer.data)
                        print(material_serializer.data)
                    else:
                        print("material_serializer._errors",
                              material_serializer._errors)
                        raise ValidationError(material_serializer.errors)

            keys = added_material[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_material)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            return Response(path_to_file)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            return Response(ex)
