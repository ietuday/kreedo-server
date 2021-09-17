import datetime
from functools import partial
from inspect import trace
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
            print("error@@", ex)
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
        # if self.request.method == 'PUT':
        #     return PlanUpdateSerailizer
        if self.request.method == 'PATCH':
            return PlanPatchUpdateSerailizer

    def put(self, request, pk):
        try:
            # print("request-----plan_activity",
            #       request.data.pop('plan_activity', None))
            print("request----",
                  request.data)
            plan_qs = Plan.objects.filter(id=pk)[0]
            print("@", plan_qs)
            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"plan_activity_dict": request.data.get('plan_activity', None)})
            plan_serializer = PlanUpdateSerailizer(plan_qs,
                                                   data=request.data, context=context, partial=True)
            if plan_serializer.is_valid():
                plan_serializer.save()
                print("Save")
                return Response(plan_serializer.data)
            else:
                return Response(plan_serializer.errors)

        except Exception as ex:
            print("error@@", ex)
            print("TRACEBACK---------", traceback.print_exc())
            logger.debug(ex)
            logger.info(ex)

            return Response(ex)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildPlanListSerializer
        if self.request.method == 'PUT':
            return ChildPlanCreateSerailizer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" School Grade Plan Api of List and Create """


class SubjectSchoolGradePlanListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SubjectSchoolGradePlan

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectSchoolGradePlanListSerializer

    def post(self, request):
        try:
            print("request---------------")
            """  Pass dictionary through Context """

            context = super().get_serializer_context()
            context.update(
                {"grade_label_data": request.data.get(
                    'grade_list', None)})

            subject_school_grade_plan = SubjectSchoolGradePlanCreateSerializer(
                data=request.data.get(
                    'grade_list', None)[0], context=context)
            if subject_school_grade_plan.is_valid():
                subject_school_grade_plan.save()
                return Response("Created")
            else:
                return Response(subject_school_grade_plan.errors)

        except Exception as ex:
            print(ex)
            print("TRACEBAK----", traceback.print_exc())
            return Response(ex)


""" School Subject Plan Api of List and Create """


class SubjectSchoolPlanListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SubjectSchoolGradePlan
 
    def post(self, request):
        try:
            print("request---------------")
            """  Pass dictionary through Context """

            context = super().get_serializer_context()
            context.update(
                {"subject_label_data": request.data.get(
                    'subject_list', None)})

            subject_school_plan = SubjectSchoolPlanCreateSerializer(
                data=request.data.get(
                    'subject_list', None)[0], context=context)
            if subject_school_plan.is_valid():
                subject_school_plan.save()
                return Response("Created")
            else:
                return Response(subject_school_plan.errors)

        except Exception as ex:
            print(ex)
            print("TRACEBAK----", traceback.print_exc())
            return Response(ex)


""" Subject school Grade Plan Api of List and Create """


class SubjectSchoolGradePlanRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SubjectSchoolGradePlan

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectSchoolGradePlanListSerializer
        if self.request.method == 'PUT':
            return SubjectSchoolGradePlanCreateSerializer
        if self.request.method == 'PATCH':
            return SubjectSchoolGradeCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Child related Activity """


class ChildActivity(GeneralClass, Mixins, ListCreateAPIView):
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


""" Grade and subject list by school"""


class GradeSubjectListBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:
            grade_subject_qs = GradeSubjectPlan.objects.filter(school=pk)
            print("grade_subject_qs------------", grade_subject_qs)
            grade_subject_plan_qs = SubjectSchoolGradePlan.objects.filter(
                grade_subjects__in=grade_subject_qs)
            print("grade_subject_plan_qs---------", grade_subject_plan_qs)

            grade_subject_serializer = SubjectSchoolGradePlanListSerializer(
                grade_subject_plan_qs, many=True)
            return Response(grade_subject_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print("ERROR--------", ex)
            print("TRACEBACK----", traceback.print_exc())
            logger.debug(ex)

            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddSubjectByGrade(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    def put(self, request):
        try:
            grade_subject_qs = SubjectSchoolGradePlan.objects.filter(grade=request.data.get('grade', None),
                                                                     school=request.data.get('school', None))
            grade_subject_serializer = SubjectSchoolGradeCreateSerializer(
                grade_subject_qs, data=request.data, many=True)
            return Response(grade_subject_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:

            logger.debug(ex)

            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


""" Grade  By School """


class GradesBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:
            grade_qs = GradeSubjectPlan.objects.filter(
                school=pk)
            grades = []
            for grade in grade_qs:
                grade_dict = {}
                grade_dict['name'] = grade.grade.name
                grade_dict['id'] = grade.grade.id
                grade_dict['school'] = grade.school.id

                grades.append(grade_dict)
                grade_dict = {}
            return Response(grades, status=status.HTTP_200_OK)
        except Exception as ex:
            print("ex-----", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# """ Add Subject by Grade"""
# class AddSubjectByGrade(RetrieveUpdateDestroyAPIView):
#     d


""" Bilk Upload Plan """


class AddPlan(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_plan = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['is_Deleted'] == False:
                    print("UPDATION")
                    plan_qs = Plan.objects.filter(id=f['id'])[0]
                    plan_qs.name = f['name']
                    plan_qs.type = f['type']
                    plan_qs.activity = f['activity']
                    plan_qs.previous_kreedo = f['previous_kreedo']
                    plan_qs.is_active = f['is_active']
                    plan_qs.save()
                    plan_serializer = PlanSerailizer(plan_qs)
                    added_plan.append(plan_serializer.data)
                elif not m.isnan(f['id']) and f['is_Deleted'] == True:
                    print("DELETION")
                    plan_qs = Plan.objects.filter(id=f['id'])[0]
                    plan_activity_qs = PlanActivity.objects.filter(
                        plan=plan_qs['id'])
                    plan_serializer = PlanSerailizer(plan_qs)
                    added_plan.append(plan_serializer.data)
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
                dict_writer.writerows(added_plan)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            # print(path_to_file)
            context = {
                "isSuccess": True, "message": "Add Plan", "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

            # return Response(path_to_file)

        except Exception as ex:
            print(traceback.print_exc())
            logger.debug(ex)
            context = {
                "isSuccess": False, "message": "Issue on Plan", "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
