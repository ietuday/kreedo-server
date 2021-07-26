from kreedo.conf.logger import CustomFormatter

from kreedo.conf import logger
import traceback

from .filters import*
from .edoofun_serializer import*
from ..models import*
from django.shortcuts import render
"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework import status

import traceback
""" GetChildListAssociatedToSectionID """


class GetChildListAssociatedToSectionID(ListCreateAPIView):
    def post(self, request):
        try:
            section_qs = AcademicSession.objects.filter(school=request.data.get(
                'school', None), section=request.data.get('section', None))
            print("section_qs-----------", section_qs)
            if len(section_qs) != 0:
                child_qs = ChildPlan.objects.filter(
                    academic_session__in=section_qs)
                print("child_qs-----", child_qs)
                if len(child_qs) != 0:

                    child_serializer = ChildPlanSectionListSerializer(
                        child_qs, many=True)

                    context = {'isSuccess': True, 'message': "Child List by Section",
                               'data': child_serializer.data, "statusCode": status.HTTP_200_OK}
                    return Response(context, status=status.HTTP_200_OK)
                else:

                    context = {'isSuccess': False, 'message': "Child List by Section Not Found",
                               'data': " ", "error": child_serializer.errors, "statusCode": status.HTTP_404_NOT_FOUND}
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            else:
                context = {'isSuccess': False, 'message': "Section Not Available",
                           'data': " ", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("@@@@@@@@@@@@22", ex)
            print("traceback", traceback.print_exc())
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
