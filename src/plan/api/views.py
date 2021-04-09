from django.shortcuts import render
from .filters import*
from .serializer import*
from plan.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response


# Create your views here.

""" Subject school Grade Plan Api of List and Create """


class SubjectSchoolGradePlanListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SubjectSchoolGradePlan

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectSchoolGradePlanListSerializer
        if self.request.method == 'POST':
            return SubjectSchoolGradePlanCreateSerializer


""" Subject school Grade Plan Api of List and Create """


class SubjectSchoolGradePlanRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SubjectSchoolGradePlan
    serializer_class = SubjectSchoolGradePlanListSerializer
