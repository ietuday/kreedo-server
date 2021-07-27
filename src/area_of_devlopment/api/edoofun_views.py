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

# GetChildListAssociatedToLicenseID

from activity.models import*

# IsPlatformUser
class GetConceptListBasedOnSubjectID(ListCreateAPIView):
    def get(self, request, pk):
        try:
            subject_qs = Activity.objects.filter(subject__in=pk)
            print("Subject-----",subject_qs)
            if subject_qs:
                skill_qs_serializer = SkillSerializer(subject_qs, many=True)

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


