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

""" Logger Function """


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")


"""  Register Child """


class RegisterChild(ListCreateAPIView):
    def post(self, request):
        try:

            child_detail = {
                "photo": request.data.get('photo', None),
                "first_name": request.data.get('first_name', None),
                "last_name": request.data.get('last_name', None),
                "date_of_birth": request.data.get('date_of_birth', None),
                "gender": request.data.get('gender', None),
                "date_of_joining": request.data.get('date_of_joining', None),
                "place_of_birth": request.data.get('place_of_birth', None),
                "blood_group": request.data.get('blood_group', None)
            }

            parent_detail = {
                "parents": request.data.get('parents', None)
            }
            academic_session_detail = {
                "academic_session": request.data.get('academic_session', None),
                "section": request.data.get('section', None),
                "grade": request.data.get('grade', None),
                "class_teacher": request.data.get('class_teacher', None),
                "curriculum_start_date": request.data.get('curriculum_start_date', None),
                "subjects": request.data.get('subjects', None)

            }

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"child_detail": child_detail, "parent_detail": parent_detail,
                 "academic_session_detail": academic_session_detail})
            try:

                child_detail_serializer = ChildRegisterSerializer(
                    data=dict(child_detail), context=context)
                if child_detail_serializer.is_valid():
                    child_detail_serializer.save()
                    return Response(child_detail_serializer.data)
                else:
                    return Response(child_detail_serializer.errors)

            except Exception as ex:
                logger.info(ex)
                logger.debug(ex)

        except Exception as ex:
            context = {"isSuccess": False, "message": "Issue in Child Creation", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
