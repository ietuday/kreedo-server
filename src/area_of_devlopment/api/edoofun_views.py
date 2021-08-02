import traceback
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from kreedo.general_views import*
from child.models import*
from .edoofun_serializer import*
from .filters import*
from session.models import*
from schools.models import*
from users.api.serializer import*
from rest_framework import status
from datetime import date

""" import Logger """

from kreedo.conf import logger
from kreedo.conf.logger import CustomFormatter
import logging



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")




""" Skill List based on concept id """




class SkillListByConcept(ListCreateAPIView):
    def get(self, request, pk):
        try:
            skill_qs = Skill.objects.filter(concept=pk)
            if skill_qs:
                skill_qs_serializer = SkillSerializer(skill_qs, many=True)

                context = {'isSuccess': True, 'message': "Skill List by Concept ID",
                                'data': skill_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': True, 'message': "Skill List by Concept ID Not found",
                                'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# GetConceptListBasedOnSubjectID


from activity.models import*

# IsPlatformUser
class GetConceptListBasedOnSubjectID(ListCreateAPIView):
    def get(self, request, pk):
        try:
            activity_qs = Activity.objects.filter(subject=pk)
            print("activity_qs-----",activity_qs)
            if activity_qs:
                skill_qs_serializer = SkillConceptSerializer(Skill.objects.filter(activity__in=activity_qs), many=True)
                print("skill_qs_serializer",skill_qs_serializer.data)
                result = []
                for data in skill_qs_serializer.data:
                    if data['concept'] not in result: 
                        result.append(data['concept'])

                context = {'isSuccess': True, 'message': "Get Concept List Based On SubjectID",
                                'data': result, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
                
            else:
                context = {'isSuccess': False, 'message': "Concept Not found",
                                'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP__NOT_FOUND)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" Skill List and Create """

class GetSkillList(ListCreateAPIView):
    model = Skill
    filterset_class = SkillFilter

    def get(self, request):
        try:
            skill_qs = Skill.objects.all()
            print("skill_qs-----",skill_qs)
            if len(skill_qs)!=0:
                skill_qs_serializer = EdooFunSkillListSerializer(skill_qs, many=True)
                print("skill_qs_serializer",skill_qs_serializer.data)
                
                context = {'isSuccess': True, 'message': "Skill List",
                                'data': skill_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
                
            else:
                context = {'isSuccess': False, 'message': "Skill List Not found",
                                'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" skill by skill id """
class GetSkillDetailBasedOnSkillId(ListCreateAPIView):
    model = Skill
    filterset_class = SkillFilter

    def get(self, request, pk):
        try:
            skill_qs = Skill.objects.filter(id=pk)
            print("skill_qs-----",skill_qs)
            if len(skill_qs)!=0:
                skill_qs_serializer = EdooFunSkillListSerializer(skill_qs, many=True)
                print("skill_qs_serializer",skill_qs_serializer.data)
                
                context = {'isSuccess': True, 'message': "Skill List",
                                'data': skill_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
                
            else:
                context = {'isSuccess': False, 'message': "Skill List Not found",
                                'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)




""" Concept List and Create """

class GetConceptList(ListCreateAPIView):
    model = Concept
    filterset_class = ConceptFilter

    def get(self, request):
        try:
            Concept_qs = Concept.objects.all()
            print("Concept_qs-----",Concept_qs)
            if len(Concept_qs)!=0:
                Concept_qs_serializer = EdooFunConceptListSerializer(Concept_qs, many=True)
                print("Concept_qs_serializer",Concept_qs_serializer.data)
                
                context = {'isSuccess': True, 'message': "Concept List",
                                'data': Concept_qs_serializer.data, "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
                
            else:
                context = {'isSuccess': False, 'message': "Concept List Not found",
                                'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

