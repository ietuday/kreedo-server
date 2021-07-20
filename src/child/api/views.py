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
from .serializer import*
from .filters import*
from session.models import*
from schools.models import*
from users.api.serializer import*
from rest_framework import status
from datetime import date




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
        if self.request.method == 'PUT':
            return ChildSerializer
    
    def patch(self, request, pk):
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

            child_qs = Child.objects.filter(id=pk)[0]
            print(parent_detail['parents'])
            child_qs_serializer = ChildUpdateSerializer(child_qs,data=dict(child_detail), partial=True)
            if child_qs_serializer.is_valid():
                child_qs_serializer.save()
                parents_detail = parent_detail['parents']
                # pdb.set_trace()
                parent_list = []
                for parent in parents_detail:

                    try:
                        if parent['id'] is None:
                            parent_serializer = ParentSerializer(data=dict(parent))
                            if parent_serializer.is_valid():
                                parent_serializer.save()
                                parent_data = {
                                    "user_obj": parent_serializer.data['id'],
                                    "relationship_with_child": parent['relationship_with_child'],
                                    "phone": parent['phone'],
                                    "gender":parent['gender'],
                                    "photo":parent['photo']

                                }
                                parent_detail_serializer = ParentDetailSerializer(
                                    data=dict(parent_data))

                                if parent_detail_serializer.is_valid():

                                    parent_detail_serializer.save()

                                    parent_id = parent_detail_serializer.data['user_obj']
                                    parent_list.append(parent_id)

                                    # self.context.update({"parent_detail_serializer_data": parent_detail_serializer.data})
                                else:
                                    raise ValidationError(
                                        parent_detail_serializer.errors)

                            else:
                                raise ValidationError(parent_serializer.errors)
                        else:
                            parent_qs = User.objects.filter(id=parent['id'])[0]
                            parent_serializer = ParentSerializer(parent_qs, data=dict(parent), partial=True)
                            if parent_serializer.is_valid():
                                parent_serializer.save()
                                parent_data = {
                                    "user_obj": parent_serializer.data['id'],
                                    "relationship_with_child": parent['relationship_with_child'],
                                    "phone": parent['phone'],
                                    "gender":parent['gender'],
                                    "photo":parent['photo']

                                }
                                parent_detail_qs = UserDetail.objects.filter(user_obj=parent_serializer.data['id'])[0]
                                parent_detail_serializer = ParentDetailSerializer(
                                    parent_detail_qs, data=dict(parent_data), partial=True)

                                if parent_detail_serializer.is_valid():

                                    parent_detail_serializer.save()

                                    parent_id = parent_detail_serializer.data['user_obj']
                                    parent_list.append(parent_id)

                                    # self.context.update({"parent_detail_serializer_data": parent_detail_serializer.data})
                                else:
                                    raise ValidationError(
                                        parent_detail_serializer.errors)

                            else:
                                raise ValidationError(parent_serializer.errors)


                    except Exception as ex:
                        logger.debug(ex)
                        logger.info(ex)
                        raise ValidationError(ex)

                child_qs.parent.set(parent_list)

                child_qs.save()

                acad_session = academic_session_detail['academic_session']
                section = academic_session_detail['section']
                grade = academic_session_detail['grade']
                class_teacher = academic_session_detail['class_teacher']

                acadmic_ids = AcademicSession.objects.filter(id=acad_session,
                                                         grade=grade, section=section, class_teacher=class_teacher).values('id')
            
                if len(acadmic_ids) is 0:
                    acadmic_ids = []
                    return Response("acadmic_ids not found", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    acadmic_ids = acadmic_ids[0]['id']
                academic_session_detail = {
                    "child":pk,
                    "academic_session": acadmic_ids,
                    "subjects": academic_session_detail['subjects'],
                    "curriculum_start_date": academic_session_detail['curriculum_start_date']
                }
                child_plan_qs = ChildPlan.objects.filter(id= request.data.get('academic_session_data', None))
                """  update child plan """
                try:

                    child_plan_serializer = ChildPlanCreateSerailizer(
                        child_plan_qs, data=dict(academic_session_detail), partial=True)
                    if child_plan_serializer.is_valid():
                        child_plan_serializer.save()

                    # self.context.update({"child_plan_serializer_data":child_plan_serializer.data})

                    else:
                        raise ValidationError(child_plan_serializer.errors)
                except Exception as ex:
                    logger.debug(ex)
                    logger.info(ex)
                    raise ValidationError(ex)

                    
            else:
                print(child_qs_serializer.errors)
                raise ValidationError(child_qs_serializer.errors)

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            return Response(ex)
    

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





""" Child Session by  Child detail """
class ChildSessionByChild(GeneralClass,Mixins,ListCreateAPIView):
    def get(self, request, pk):
        try:
            child_detail_qs = ChildSession.objects.filter(child=pk)
            child_detail_serializer = ChildSessionListSerializer(child_detail_qs, many=True)
            return Response(child_detail_serializer.data,status = status.HTTP_200_OK)
            
        except Exception as ex:
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" Child According Child detail """
class ChildDetailByChild(GeneralClass,Mixins,ListCreateAPIView):
    def get(self, request, pk):
        try:
            child_detail_qs = ChildDetail.objects.filter(child=pk)[0]
            child_detail_serializer = ChildDetailListSerializer(child_detail_qs)
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
            academic_session = AcademicSession.objects.filter(
                grade=grade, section=section)
            print("academic_session",academic_session)
            print("academic_session",len(academic_session))

            if len(academic_session) != 0:
                child_query = ChildPlan.objects.filter(
                    academic_session=academic_session[0], subjects=subject,curriculum_start_date__lte=date.today())
                
                child_serailizer = ChildPlanListSerializer(child_query, many=True)

            # context = {"message": "Child List According to grade",
            #            "data": child_serailizer.data, "statusCode": status.HTTP_200_OK}
                return Response(child_serailizer.data,status=status.HTTP_200_OK)
            else:
                return Response("academic_session not available",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            print("#############",ex)
            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from plan.api.serializer import*
class AttendenceByAcademicSession(ListCreateAPIView):
    def post(self, request):
        try:
            grade = request.data.get('grade', None)
            section = request.data.get('section', None)
            attendance_date = request.data.get('attendance_date', None)
            

            period_detail = {
                "period": request.data.get('period', None),
                "activity": request.data.get('activity', None)
            }
            context = super().get_serializer_context()
            context.update({"period_detail": period_detail})


            academic_id = AcademicSession.objects.filter(
                grade=grade, section=section)
        
            if len(academic_id) is not 0:
                
                academic_qs_serializer = AcademicSessionForCalender(academic_id[0])

                attendence_qs = Attendance.objects.filter(academic_session=academic_id[0],attendance_date= attendance_date)
                if len(attendence_qs)is not 0:
                    print("attendence_qs",attendence_qs)
                    
                    attendanceListSerializer = AttendanceListSerializer(attendence_qs[0],context=context)
                    context = {"isSuccess": True, "message": "Child List",
                    "error": "", "data": attendanceListSerializer.data}
                    return Response(context, status=status.HTTP_200_OK)
                    # return Response(attendanceListSerializer.data, status=status.HTTP_200_OK)
                # else:

                #     context = {"isSuccess": False, "message": "Issue in Attendace",
                #         "error": "Attendance is not available", "data": ""}
                #     return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@")
                    child_qs = ChildPlan.objects.filter(academic_session=academic_id[0])
                    child_qs_serializer = ChildPlansChildSerializer(child_qs, many=True)
                    child_list =[]
                    child_data = {
                        "marked_status":False,
                        "childs":ChildJsonData(child_qs_serializer.data,period_detail),
                        "attendance_date":"",
                        "is_active":False

                    }
                    child_list.append(child_data)
                    context = {"isSuccess": True, "message": "Child List",
                    "error": "", "data": child_list}
                    return Response(context, status=status.HTTP_200_OK)

            else:
                context = {"isSuccess": False, "message": "Issue in Child List",
                    "error": "Grade Section is not valid", "data": ""}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
        except Exception as ex:
            print("ERROR--", ex)
            print("traceback----", traceback.print_exc())
            logger.info(ex)
            logger.debug(ex)
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Child Bulk Upload """
class AddChild(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            print("File in memory", file_in_memory)

            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            print("df",df)
            added_child = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['is_Deleted'] == False:
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
                    child_serializer = ChildSerializer(child_qs)
                    added_child.append(child_serializer.data)
                    parents_data = f.get('parents_id', None)
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

                elif not m.isnan(f['id']) and f['is_Deleted'] == True:
                    print("DELETION")
                    child_qs = Child.objects.filter(id=f['id'])[0]
                    child_plan_qs = ChildPlan.objects.filter(child = child_qs['id'])[0]
                    for i in child_qs['parents']:
                        user_qs = User.objects.filter(id=i)[0]
                        user_detail_qs = UserDetail.objects.filter(user_obj=user_qs['id'])[0]
                        user_detail_qs.delete()
                        user_qs.delete()
                    child_serializer = ChildSerializer(child_qs)
                    added_child.append(child_serializer.data)
                    child_plan_qs.delete()
                    child_qs.delete()


                else:
                    print("Create")
                    print(" f.get('parents',None)", f.get('parents',None))

                    parent_detail = f.get('parents',None)
                    parent_list = []
                    for i, da in enumerate(json.loads(parent_detail), start=1):
                        print("da---->",da)

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
                                print("parent")
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
                    print("Child----", child_data)
                    try:
                        child_serializer = ChildSerializer(
                        data=dict(child_data))
                        if child_serializer.is_valid():
                            child_serializer.save()
                            print("child Create")
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
                        print("da",da['academic_calender'])
                        acadmic_ids = AcademicSession.objects.filter(academic_calender=da['academic_calender'],
                                                         grade=da['grade'], section=da['section'], class_teacher=da['class_teacher']).values('id')

                        if len(acadmic_ids) != 0: 

                            acadmic_ids = acadmic_ids[0]['id']
                            print("####", acadmic_ids)
                            child_plan_data = {
                                "child":child_serializer.data['id'],
                                "academic_session":acadmic_ids,
                                "subjects": da['subjects'],
                                "class_teacher": da['class_teacher'],
                                "curriculum_start_date": da['curriculum_start_date'],
                                "is_active":"TRUE"
                            }
                            try:
                                childplan_serializer = ChildPlanCreateSerailizer(data=dict(child_plan_data))
                                if childplan_serializer.is_valid():
                                    childplan_serializer.save()
                                    # added_child.append(childplan_serializer.data)
                                    print("child_plan Create")
                                    
                                else:
                                    raise ValidationError(childplan_serializer.errors)
                            except Exception as ex:
                                print("error", ex)
                                print("traceback", traceback.print_exc())
                                logger.debug(ex)
                                return Response(ex)
                        else:
                            print("acadmic_ids not found")

            keys = added_child[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_child)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "Child Added sucessfully",
            "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print("ERROR-------", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            context = {"isSuccess": False, "message": "Issue in child",
            "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Bulk Upload Child Detail """


import math


class AddChildDetail(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_child = []

            for i, f in enumerate(df, start=1):
                # f['subject'] = json.loads(f['subject'])
                
                if not math.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    child_detail_qs = ChildDetail.objects.filter(id=f['id'])[0]
                    child_detail_qs.child = f['child']
                    child_detail_qs.medical_details = f['medical_details']
                    child_detail_qs.residence_details = f['residence_details']
                    child_detail_qs.emergency_contact_details = f['emergency_contact_details']
                    child_detail_qs.residence_details = f['residence_details']
                    child_detail_qs.siblings = f['siblings']
                    child_detail_qs.documents = json.loads(f['documents'])
                    child_detail_qs.save()
                    added_child.append(child_detail_qs)
                elif not math.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    child_detail_qs = ChildDetail.objects.filter(id=f['id'])[0]
                    added_child.append(child_detail_qs)
                    child_detail_qs.delete()
                else:  
                    print("Create")
                    # f['subject'] = json.loads(f['subject'])
                    child_detail_serializer = ChildDetailCreateSerializer(
                        data=dict(f))
                    if child_detail_serializer.is_valid():
                        child_detail_serializer.save()
                        added_child.append(
                            child_detail_serializer.data)
                        print(child_detail_serializer.data)
                    else:
                        print("child_detail_serializer._errors",
                            child_detail_serializer._errors)
                        raise ValidationError(child_detail_serializer.errors)

            keys = added_child[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_child)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "Child Detail Added sucessfully",
            "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            # return Response(ex)
            context = {"isSuccess": False, "message": "Issue Child Detail",
            "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Bulk  upload child Session """

class AddChildSession(ListCreateAPIView):

    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_child = []

            for i, f in enumerate(df, start=1):
                # f['subject'] = json.loads(f['subject'])
                
                if not math.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    child_detail_qs = ChildSession.objects.filter(id=f['id'])[0]
                    child_detail_qs.child = f['child']
                    child_detail_qs.session_name = f['session_name']
                    child_detail_qs.session_type = f['session_type']
                    child_detail_qs.academic_session = f['academic_session']
                    child_detail_qs.start_date = f['start_date']
                    child_detail_qs.end_date = f['end_date']
                    child_detail_qs.is_active = json.loads(f['is_active'])
                    child_detail_qs.save()
                    added_child.append(child_detail_qs)
                elif not math.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    child_detail_qs = ChildSession.objects.filter(id=f['id'])[0]
                    added_child.append(child_detail_qs)
                    child_detail_qs.delete()
                else:  
                    print("Create")
                    # f['subject'] = json.loads(f['subject'])
                    child_session_serializer = ChildSessionCreateSerializer(
                        data=dict(f))
                    if child_session_serializer.is_valid():
                        child_session_serializer.save()
                        added_child.append(
                            child_session_serializer.data)
                        print(child_session_serializer.data)
                    else:
                        print("child_session_serializer._errors",
                            child_session_serializer._errors)
                        raise ValidationError(child_session_serializer.errors)

            keys = added_child[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_child)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file('output.csv', 'kreedo-new' , 'files/output.csv')
            path_to_file =  'https://' + str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "Child Session Added sucessfully",
            "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print("error", ex)
            print("traceback", traceback.print_exc())
            logger.debug(ex)
            # return Response(ex)
            context = {"isSuccess": False, "message": "Issue Child Session",
            "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







