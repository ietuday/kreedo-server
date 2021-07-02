from django.shortcuts import render


from .serializer import*
from area_of_devlopment.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from .filters import*

""" 
    Packages for uploading csv
"""
import pandas as pd
import math as m
import json
import csv
import traceback
from kreedo.conf import logger
from users.api.custum_storage import FileStorage
from kreedo.conf.logger import CustomFormatter
import logging
import ast
from rest_framework import status

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


""" Area of Devlopment List and Create """


class AreaOfDevlopmentListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = AreaOfDevlopment
    filterset_class = AreaOfDevlopmentFilter
    serializer_class = AreaOfDevlopmentSerializer


""" Area of Devlopment Update and Delete """


class AreaOfDevlopmentRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = AreaOfDevlopment
    filterset_class = AreaOfDevlopmentFilter
    serializer_class = AreaOfDevlopmentSerializer


""" Concept List and Create """


class ConceptListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Concept
    filterset_class = ConceptFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConceptListSerializer
        if self.request.method == 'POST':
            return ConceptCreateSerializer


""" Retrive update and delete Concept """


class ConceptRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Concept
    filterset_class = ConceptFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConceptListSerializer
        if self.request.method == 'PUT':
            return ConceptCreateSerializer
        if self.request.method == 'DELETE':
            return ConceptListSerializer


""" Skill List and Create """


class SkillListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Skill
    filterset_class = SkillFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SkillListSerializer
        if self.request.method == 'POST':
            return SkillCreateSerializer


""" Skill Update And Retrive """


class SkillRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Skill
    filterset_class = SkillFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SkillListSerializer
        if self.request.method == 'PUT':
            return SkillCreateSerializer
        if self.request.method == 'DELETE':
            return SkillListSerializer


""" Cocept and Skill Bulk Upload """
class AddConceptSkill(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_conept_skill = []

            for i, f in enumerate(df, start=1):
                # f.get('aod',None)
                f['activity']= ast.literal_eval(f['activity'])
                f['remed_activity']= ast.literal_eval(f['remed_activity'])
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    concept_qs = Concept.objects.filter(id=f['id'])[0]
                    concept_qs.name = f['concept_name']
                    concept_qs.description = f['concept_description']
                    concept_qs.aod = f['aod']
                    concept_qs.is_active = f['is_active']
                    concept_qs.save()
                    skill_qs = Skill.objects.filter(id=f['skill_id'],concept=f['id'])
                    skill_qs.name= f['skill_name']
                    skill_qs.description=f['skill_description']
                    skill_qs.threshold_percentage=f['threshold_percentage']
                    skill_qs.activity = f['activity']
                    skill_qs.remed_activity=f['remed_activity']
                    skill_qs.save()
                    # added_conept_skill.append(concept_qs)
                    added_conept_skill.append(skill_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    concept_qs = Concept.objects.filter(id=f['id'])[0]
                    skill_qs = Skill.objects.filter(id=f['skill_id'],concept=concept_qs['id'])
                    # added_conept_skill.append(concept_qs)
                    added_conept_skill.append(skill_qs)
                    concept_qs.delete()
                    skill_qs.delete()
                else:
                    print("Create")
                    concept_data = {
                        "name":f.get('concept_name',None),
                        "description":f.get('concept_description',None),
                        "aod":f.get('aod',None),
                        "is_active":"TRUE"
                    }
                    try:
                    
                        conept_serializer = ConceptCreateSerializer(
                            data=dict(concept_data))
                        if conept_serializer.is_valid():
                            conept_serializer.save()
                            # added_conept_skill.append(
                            #     conept_serializer.data)
                            print(conept_serializer.data)
                        else:
                            
                            raise ValidationError(conept_serializer.errors)
                    except Exception as ex:
                        print("error", ex)
                        print("traceback", traceback.print_exc())
                        logger.debug(ex)
                        return Response(ex)
                

                    skill_data = {

                        "name":f.get('skill_name', None),
                        "description":f.get('skill_description', None),
                        "concept":conept_serializer.data['id'],
                        "is_active":"TRUE",
                        "threshold_percentage":f.get('threshold_percentage', None),
                        "activity":f['activity'],
                        "remed_activity":f['activity'],
                    }
                    try:
                        skill_serializer = SkillCreateSerializer(
                            data=dict(skill_data))
                        if skill_serializer.is_valid():
                            skill_serializer.save()
                            print("skill_serializer.data",skill_serializer.data)
                            added_conept_skill.append(
                                skill_serializer.data)
                           
                        else:
                            raise ValidationError(skill_serializer.errors)
                    except Exception as ex:
                        print("error", ex)
                        print("traceback", traceback.print_exc())
                        logger.debug(ex)
                        return Response(ex)
                

            keys = added_conept_skill[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_conept_skill)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            # print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "Concept Skill Added sucessfully",
                "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)
            # return Res

        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
            logger.debug(ex)
            context = {"isSuccess": False, "message": "Issue Skill Concept",
                "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



