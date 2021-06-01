import traceback
from django.shortcuts import render
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from kreedo.general_views import*
from child.models import*
from .serializer import*
from .filters import*
from session.models import*
from schools.models import*
from users.api.serializer import*
from rest_framework import status
from datetime import date

from rest_framework.response import Response



""" 
    Packages for uploading csv
"""
import pandas as pd
import math as m
import json
import csv
import traceback
from kreedo.conf import logger
from rest_framework.response import Response
from users.api.custum_storage import FileStorage
from kreedo.conf.logger import CustomFormatter
import logging

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


""" create and List Child """


class ChildListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Child
    filterset_class = ChildFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildListSerializer

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
                "parents": request.data.get('parent', None)
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

                child_detail_serializer = ChildCreateSerializer(
                    data=dict(child_detail), context=context)
                if child_detail_serializer.is_valid():
                    child_detail_serializer.save()
                    return Response(child_detail_serializer.data)
                else:
                    return Response(child_detail_serializer.errors)

            except Exception as ex:
                logger.info(ex)
                logger.debug(ex)
                return Response(ex)

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            return Response(ex)


""" Child Retrive , Update ,Destroy  """
class ChildRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Child
    filterset_class = ChildFilter


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildSerializer
        if self. request.method == 'PATCH':
            return ChildSerializer
        if self.request.method == 'POST':
            return ChildSerializer
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Update Child """


class ChildDetailListCreate(GeneralClass, Mixins, CreateAPIView):
    model = ChildDetail
    filterset_class = ChildDetailFilter


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildDetailListSerializer

        if self.request.method == 'POST':
            return ChildDetailCreateSerializer
        if self.request.method == 'PATCH':
            return ChildDetailCreateSerializer
        
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class ChildDetailRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = ChildDetail
    filterset_class = ChildDetailFilter


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildDetailListSerializer

        if self.request.method == 'PUT':
            return ChildDetailCreateSerializer
         
        if self.request.method == 'PATCH':
            return ChildDetailCreateSerializer

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)



""" Child Session Create Serializer """
class ChildSessionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = ChildSession
    filterset_class = ChildSessionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildSessionListSerializer

        if self.request.method == 'POST':
            return ChildSessionCreateSerializer

"""  Child Session Retrive Delete update """
class ChildSessionRetriveUpdateDestroy(GeneralClass,Mixins,RetrieveUpdateDestroyAPIView):
    model = ChildSession
    filterset_class = ChildSessionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildSessionListSerializer

        if self.request.method == 'PUT':
            return ChildSessionCreateSerializer

        if self.request.method == 'PATCH':
            return ChildSessionCreateSerializer
        
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)








""" Child According Child detail """
class ChildDetailByChild(GeneralClass,Mixins,ListCreateAPIView):
    def get(self, request, pk):
        try:
            child_detail_qs = ChildDetail.objects.filter(child=pk)
            child_detail_serializer = ChildDetailListSerializer(child_detail_qs, many=True)
            return Response(child_detail_serializer.data,status = status.HTTP_200_OK)
            
        except Exception as ex:
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
""" Attendance List and Create """


class AttendanceListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Attendance
    filterset_class = AttendanceFilter


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AttendanceListSerializer

        if self.request.method == 'POST':
            return AttendanceCreateSerializer


""" Attendance Retrive Update and Delete """


class AttendanceRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Attendance
    filterset_class = AttendanceFilter
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AttendanceListSerializer

        if self.request.method == 'PUT':
            return AttendanceCreateSerializer

        if self.request.method == 'DELETE':
            return AttendanceListSerializer


""" child List of class, section and subject """

class childListAccordingToClass(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            grade = request.data.get('grade', None)
            section = request.data.get('section', None)
            subject = request.data.get('subject', None)
            academic_id = AcademicSession.objects.get(
                grade__name=grade, section__name=section).id
            subject = Subject.objects.get(name=subject).name

            child_query = ChildPlan.objects.filter(
                academic_session=academic_id, subjects__name=subject,curriculum_start_date__lte=date.today())
            
            child_serailizer = ChildPlanListSerializer(child_query, many=True)

            # context = {"message": "Child List According to grade",
            #            "data": child_serailizer.data, "statusCode": status.HTTP_200_OK}
            return Response(child_serailizer.data,status=status.HTTP_200_OK)

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttendenceByAcademicSession(GeneralClass,Mixins,ListCreateAPIView):
    def post(self, request):
        try:
            grade = request.data.get('grade', None)
            section = request.data.get('section', None)
            attendance_date = request.data.get('attendance_date', None)
            academic_id = AcademicSession.objects.get(
                grade=grade, section=section).id

            attendence_qs = Attendance.objects.filter(academic_session=academic_id,attendance_date= attendance_date)
            attendanceListSerializer = AttendanceListSerializer(attendence_qs, many=True)
            # context = {"message": "Attendence By Academic Session",
            #            "data": attendanceListSerializer.data, "statusCode": status.HTTP_200_OK}
            return Response(attendanceListSerializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Child Bulk Upload """
class AddChild(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_child = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    child_qs = Child.objects.filter(id=f['id'])[0]
                    child_qs.first_name = f['first_name']
                    child_qs.last_name = f['last_name']
                    child_qs.date_of_birth = f['date_of_birth']
                    child_qs.gender = f['gender']
                    child_qs.date_of_joining = f['date_of_joining']
                    child_qs.place_of_birth = f['place_of_birth']
                    child_qs.blood_group = f['blood_group']
                    child_qs.photo = f['photo']
                    child_qs.is_active = f['is_active']
                    child_qs.save()
                    child_plan_data = f.get('child_plan', None)
                    print(child_plan_data)
                    for i, da in enumerate(json.loads(child_plan_data), start=1):
                        child_plan_qs = ChildPlan.objects.filter(child=child_qs['id'])[0]
                        child_plan_qs.academic_session = da['academic_session']
                        child_plan_qs.subjects = da['subjects']
                        child_plan_qs.class_teacher = da['class_teacher']
                        child_plan_qs.curriculum_start_date = da['curriculum_start_date']
                        child_plan_qs.save()
                    added_child.append(child_qs)
                    parents_data = f.get('parents', None)
                    print(parents_data)
                    for i in parents_data:
                        auth_user = User.objects.filter(user_obj=i)[0]
                        auth_user.first_name = f.get('first_name', None)
                        auth_user.last_name = f.get('last_name', None)
                        auth_user.email = f.get('email', None)
                        auth_user.save()
                        user_detail_qs = UserDetail.objects.filter(user_obj=i)[0]
                        user_detail_qs.phone = f.get('phone', None)
                        user_detail_qs.joining_date = f.get('joining_date', None)
                        user_detail_qs.save()

                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    child_qs = Child.objects.filter(id=f['id'])[0]
                    child_plan_qs = ChildPlan.objects.filter(child = child_qs['id'])[0]
                    for i in child_qs['parents']:
                        user_qs = User.objects.filter(id=i)[0]
                        user_detail_qs = UserDetail.objects.filter(user_obj=user_qs['id'])[0]
                        user_detail_qs.delete()
                        user_qs.delete()
                    added_child.append(child_qs)
                    child_plan_qs.delete()
                    child_qs.delete()


                else:
                    print("Create")
                    parent_detail = f.get('parents',None)
                    parent_list = []
                    for i, da in enumerate(json.loads(parent_detail), start=1):
                        print("da",da)

                        """ Create Auth User"""
                        user_data = {
                                "first_name":da['first_name'],
                                "last_name":da['last_name'],
                                "email":da['email'],
                                "is_active":"TRUE"

                        }
                        user_data_serializer = ParentSerializer(data=dict(user_data))
                        if user_data_serializer.is_valid():
                            user_data_serializer.save()
                        else:
                            raise ValidationError(user_data_serializer.errors)

                        user_details_data = {
                                "user_obj":user_data_serializer.data['id'],
                                "phone":da['phone'],
                                "gender":da['gender'],
                                "email":da['email'],
                                "relationship_with_child":da['relationship_with_child']
                        } 
                        try:
                            user_details_data_serializer = ParentDetailSerializer(
                                data=dict(user_details_data))

                            if user_details_data_serializer.is_valid():

                                user_details_data_serializer.save()
                                parent_id = user_details_data_serializer.data['user_obj']
                                parent_list.append(parent_id)
                            else:
                                raise ValidationError(user_details_data_serializer.errors)
                        except Exception as ex:
                            print("error", ex)
                            print("traceback", traceback.print_exc())
                            logger.debug(ex)
                            return Response(ex)
                


                    """ Child Creation """
                    child_data = {
                        "first_name":f.get('first_name', None),
                        "last_name":f.get('last_name', None),
                        "date_of_birth":f.get('date_of_birth', None),
                        "gender":f.get('gender', None),
                        "date_of_joining":f.get('date_of_joining', None),
                        "place_of_birth":f.get('place_of_birth', None),
                        "blood_group":f.get('blood_group', None),
                        "photo":f.get('photo', None),
                        "parent":parent_list

                    }
                    try:
                        child_serializer = ChildSerializer(
                        data=dict(child_data))
                        if child_serializer.is_valid():
                            child_serializer.save()
                            added_child.append(
                                child_serializer.data)
                            print(child_serializer.data)
                        else:
                            raise ValidationError(child_serializer.errors)
                    except Exception as ex:
                        print("error", ex)
                        print("traceback", traceback.print_exc())
                        logger.debug(ex)
                        return Response(ex)
                
                    
                    
                    """ Child Plan Creation """
                    child_plan_data = f.get('child_plan', None)
                    print(child_plan_data)
                    for i, da in enumerate(json.loads(child_plan_data), start=1):
                        print("da",da)
                        acadmic_ids = AcademicSession.objects.filter(id=da['acad_session'],
                                                         grade=da['grade'], section=da['section'], class_teacher=da['class_teacher']).values('id')[0]['id']

                        child_plan_data = {
                            "child":child_serializer.data['id'],
                            "academic_session":acadmic_ids,
                            "subjects": da['subjects'],
                            "class_teacher": da['class_teacher'],
                            "curriculum_start_date": da['curriculum_start_date'],
                            "is_active":"TRUE"
                        }
                        try:
                            childplan_serializer = ChildPlanCreateSerailizer(data=dict(school_package_detail))
                            if childplan_serializer.is_valid():
                                childplan_serializer.save()
                                added_child.append(
                                childplan_serializer.data)
                            else:
                                raise ValidationError(childplan_serializer.errors)
                        except Exception as ex:
                            print("error", ex)
                            print("traceback", traceback.print_exc())
                            logger.debug(ex)
                            return Response(ex)

            keys = added_child[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_material)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            return Response(path_to_file)

        except Exception as ex:
           
            logger.debug(ex)
            return Response(ex)

