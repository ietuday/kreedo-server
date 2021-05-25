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
from rest_framework import status

""" 
    Packages for uploading csv
"""
import pandas as pd
import math as m
import json
import csv
import traceback
from rest_framework.response import Response
from users.api.custum_storage import FileStorage

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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlanListSerailizer
        if self.request.method == 'PUT':
            return PlanCreateSerailizer
        if self.request.method == 'DELETE':
            return PlanListSerailizer


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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectSchoolGradePlanListSerializer
        if self.request.method == 'PUT':
            return SubjectSchoolGradePlanCreateSerializer
        if self.request.method == 'DELETE':
            return SubjectSchoolGradePlanCreateSerializer


""" Child related Activity """


class ChildActivity(GeneralClass,Mixins,ListCreateAPIView):
    def post(self, request):
        try:
            child_plan = ChildPlan.objects.filter(
                child=request.data.get('child', None))
            child_plan_qs = ChildPlanActivitySerializer(child_plan, many=True)
            # context = {"message": "Activity List by Child", "isSuccess": True,
            #            "data": child_plan_qs.data, "statusCode": status.HTTP_200_OK}
            return Response(child_plan_qs.data, status=status.HTTP_200_OK)

        except Exception as ex:

            logger.debug(ex)
            # context = {"error": ex,
            #            "isSuccess": False,
            #            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Bilk Upload Plan """


class AddPlan(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_plan = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    plan_qs = Plan.objects.filter(id=f['id'])[0]
                    plan_qs.name = f['name']
                    plan_qs.type = f['type']
                    plan_qs.activity = f['activity']
                    plan_qs.is_active = f['is_active']
                    plan_qs.save()
                    added_plan.append(plan_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    plan_qs = Plan.objects.filter(id=f['id'])[0]
                    plan_activity_qs = PlanActivity.objects.filter(
                        plan=plan_qs['id'])
                    added_plan.append(plan_qs)
                    plan_qs.delete()
                else:
                    print("Create")

                    plan_serializer = PlanSerailizer(
                        data=dict(f))
                    if plan_serializer.is_valid():
                        plan_serializer.save()
                        added_plan.append(
                            plan_serializer.data)
                        print(plan_serializer.data)
                    else:

                        raise ValidationError(plan_serializer.errors)

                    activity_data = f.get('activity', None)
                    print(activity_data)
                    for i, da in enumerate(json.loads(activity_data), start=1):
                        print("da", da)
                        activity_detail = {
                            "plan": plan_serializer.data['id'],
                            "activity": da['activity'],
                            "sort_no": f.get('sort_no', None),
                            "dependent_on": f.get('dependent_on', None)
                        }

                        plan_activity_Serializer = PlanActivityCreateSerializer(
                            data=dict(activity_detail))
                        if plan_activity_Serializer.is_valid():
                            plan_activity_Serializer.save()
                        else:
                            raise ValidationError(
                                plan_activity_Serializer.errors)

            keys = added_plan[0].keys()
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

            logger.debug(ex)
            return Response(ex)
