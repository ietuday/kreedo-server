from django.shortcuts import render
from .serializer import*
from plan.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from .filters import*

# Create your views here.

""" plan Create and List """


class PlanListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Plan
    filterset_class = PlanFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlanListSerailizer
        if self.request.method == 'POST':
            return PlanCreateSerailizer


""" Plan Retrive Update Delet """


class PlanRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Plan
    filterset_class = PlanFilter
    serializer_class = PlanListSerailizer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlanListSerailizer
        if self.request.method == 'PUT':
            return PlanCreateSerailizer


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
