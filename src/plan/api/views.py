from django.shortcuts import render
from .serializer import*
from plan.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from .filters import*
from kreedo.conf.logger import CustomFormatter
import logging
# Create your views here.


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("VIEW CAlled ")

""" plan Create and List """


class PlanListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Plan
    filterset_class = PlanFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlanListSerailizer

    def post(self, request):
        try:

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"plan_activity_dict": request.data.get('plan_activity', None)})
            plan_serializer = PlanCreateSerailizer(
                data=request.data, context=context)
            if plan_serializer.is_valid():
                plan_serializer.save()
                return Response(plan_serializer.data)
            else:
                return Response(plan_serializer.errors)
        except Exception as ex:
            logger.debug(ex)
            logger.info(ex)
            
            return Response(ex)


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


""" Child Plan List and create """


class ChildPlanListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = ChildPlan
    filterset_class = ChildPlanFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildPlanListSerializer
        if self.request.method == 'POST':
            return ChildPlanCreateSerailizer


""" Child Plan Retrive Update and Delete """


class ChildPlanRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = ChildPlan
    filterset_class = ChildPlanFilter
    serializer_class = ChildPlanListSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildPlanListSerializer
        if self.request.method == 'PUT':
            return ChildPlanCreateSerailizer


""" Plan Activity List Create """


class PlanActivityListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = PlanActivity
    filterset_class = PlanActivityFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlanActivityListSerializer
        if self.request.method == 'POST':
            return PlanActivityCreateSerializer


""" Plan Activity Retrive Update And Delete """


class PlanActivityRetriveUpdateDestroy(GeneralClass, Mixins,  RetrieveUpdateDestroyAPIView):
    model = PlanActivity
    filterset_class = PlanActivityFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlanActivityListSerializer
        if self.request.method == 'PUT':
            return PlanActivityCreateSerializer


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
