import itertools
import ast
from session.api.serializer import*
from collections import ChainMap
from .utils import*
import logging
from kreedo.conf.logger import CustomFormatter
from users.api.custum_storage import FileStorage
from kreedo.conf import logger
import traceback
import csv
import json
import math as m
import pandas as pd
from address.api.serializer import AddressSerializer
from .filters import*
from .serializer import*
from schools.models import*
from kreedo.general_views import *
from django.shortcuts import render
from session.api.serializer import *
"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework import status
import pdb
from users.api.serializer import *


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


""" Grade List and Create """
# @permission_classes((IsAuthenticatedOrReadOnly,))


class GradeListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Grade
    serializer_class = GradeSerializer
    filterset_class = GradeFilter


""" Grade Retrive Update Delete """


class GradeRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Grade
    filterset_class = GradeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GradeSerializer
        if self.request.method == 'PUT':
            return GradeSerializer
        if self.request.method == 'PATCH':
            return GradeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Section List and Create """


class SectionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Section
    filterset_class = SectionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionListSerializer
        if self.request.method == 'POST':
            return SectionCreateSerializer


""" Section Retrive Update delete """


class SectionRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Section
    filterset_class = SectionFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionListSerializer
        if self.request.method == 'PUT':
            return SectionCreateSerializer
        if self.request.method == 'PATCH':
            return SectionCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Subject List and Create """


class SubjectListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Subject
    filterset_class = SubjectFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectListSerializer
        # if self.request.method == 'POST':
        #     return SubjectCreateSerializer


class SubjectCreate(Mixins, ListCreateAPIView):
    model = Subject
    filterset_class = SubjectFilter

    def post(self, request):
        try:
            print("REQUEST-----", request.data)
            if Subject.objects.filter(name=request.data.get('name')).exists():
                context = {
                    "isSuccess": False, "status": 200, "message": "Subject with this name already exists",
                    "data": []
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                subject_serializer = SubjectCreateSerializer(data=request.data)
                if subject_serializer.is_valid():
                    subject_serializer.save()
                    print("save")
                    context = {
                        "isSuccess": True, "status": 200, "message": "Subject created successfully",
                        "data": subject_serializer.data
                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context = {
                        "isSuccess": False, "status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": subject_serializer.errors,
                        "data": []
                    }
                    return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print("ERROR----->", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Subject List By School """


class SubjectListBySchool(GeneralClass, Mixins, ListCreateAPIView):
    model = Subject
    filterset_class = SubjectFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectListBySchoolSerializer


""" Subject update Retrive and Delete """


class SubjectRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Subject
    filterset_class = SubjectFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubjectListSerializer
        if self.request.method == 'PUT':
            return SubjectCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" License List and Create """


class LicenseListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = License
    filterset_class = LicenseFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LicenseListSerializer
        if self.request.method == 'POST':
            return LicenseCreateSerializer


""" License update Retrive and Delete """


class LicenseRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = License
    filterset_class = LicenseFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LicenseListSerializer
        if self.request.method == 'PUT':
            return LicenseCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" School List and Create """


class SchoolListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = School
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolListSerializer

    def post(self, request):
        try:

            address_detail = {
                "country": request.data.get('country', None),
                "state": request.data.get('state', None),
                "city": request.data.get('city', None),
                "address": request.data.get('address', None),
                "pincode": request.data.get('pincode', None),
            }
            address_serializer = AddressSerializer(data=address_detail)
            if address_serializer.is_valid():
                address_serializer.save()
            else:
                raise serializers.ValidationError(
                    "address_serializer._errors", address_serializer._errors)
            licence_detail = {
                "total_no_of_user": request.data.get('total_no_of_user', None),
                "total_no_of_children": request.data.get('total_no_of_children', None),
                "licence_from": request.data.get('licence_start_date', None),
                "licence_till": month_calculation(request.data.get('licence_start_date', None), request.data.get('no_of_months', None)),

            }
            print("licence_detail", licence_detail)
            licenseCreateSerializer = LicenseCreateSerializer(
                data=dict(licence_detail))

            if licenseCreateSerializer.is_valid():
                licenseCreateSerializer.save()
            else:
                raise ValidationError(licenseCreateSerializer.errors)

            school_data = {
                "name": request.data.get('name', None),
                "type": request.data.get('type', None),
                "logo": request.data.get('logo', None),
                "address": address_serializer.data['id'],
                "license": licenseCreateSerializer.data['id'],
                "is_active": request.data.get('is_active', None),
            }

            context = self.get_serializer_context()
            context.update({"school_data": school_data,
                            "school_package_dict": request.data.get('school_package', None)})

            school_serializer = SchoolSerializer(
                data=dict(school_data), context=context)
            if school_serializer.is_valid():
                school_serializer.save()
                return Response(school_serializer.data)
            return Response(school_serializer.errors)

            school_calender_detail = {
                "school": school_serializer.data['id'],
                "session_from": datetime.date.today(),
                "session_till": addYears(datetime.date.today(), request.data.get('school_calender_for_no_of_yrs', None)),
            }

            schoolCalendarCreateSerializer = SchoolCalendarCreateSerializer(
                data=dict(school_calender_detail))

            if schoolCalendarCreateSerializer.is_valid():
                schoolCalendarCreateSerializer.save()
            else:
                raise ValidationError(schoolCalendarCreateSerializer.errors)

        except Exception as ex:
            logger.debug(ex)
            return Response(ex)


""" School update Retrive and Delete """


class SchoolRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = School
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SchoolDetailListSerializer
        # if self.request.method == 'PUT':
        #     return SchoolSerializer
        if self.request.method == 'PATCH':
            return SchoolSerializer

    def put(self, request, pk):
        try:

            school_data = {
                "name": request.data.get('name', None),
                "type": request.data.get('type', None),
                "logo": request.data.get('logo', None),
                "address": request.data.get('address_id', None)

            }
            address_detail = {
                "country": request.data.get('country', None),
                "state": request.data.get('state', None),
                "city": request.data.get('city', None),
                "address": request.data.get('address', None),
                "pincode": request.data.get('pincode', None),
            }
            address_qs = Address.objects.get(
                id=request.data.get('address_id', None))

            address_qs_serializer = AddressSerializer(
                address_qs, data=dict(address_detail), partial=True)
            if address_qs_serializer.is_valid():
                address_qs_serializer.save()
            else:
                raise ValidationError(address_qs.errors)
            school_qs = School.objects.get(id=pk)

            school_qs_serailzer = SchoolUpdateSerializer(
                school_qs, data=dict(school_data), partial=True)
            if school_qs_serailzer.is_valid():
                school_qs_serailzer.save()
                return Response(school_qs_serailzer.data, status=status.HTTP_200_OK)
            else:
                print("errors------>", school_qs_serailzer.errors)
                return Response(school_qs_serailzer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print("TRaceback-----", traceback.print_exc())
            print("ERROR----------->", ex)
            logger.debug(ex)
            return Response(ex)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Section Subject Teacher List and Create """


class SectionSubjectTeacherListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SectionSubjectTeacher

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionSubjectTeacherListSerializer
        if self.request.method == 'POST':
            return SectionSubjectTeacherCreateSerializer


"""Section Subject Teacher  update Retrive and Delete """


class SectionSubjectTeacherRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = SectionSubjectTeacher
    serializer_class = SectionSubjectTeacherCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SectionSubjectTeacherListSerializer
        if self.request.method == 'PUT':
            return SectionSubjectTeacherCreateSerializer
        if self.request.method == 'PATCH':
            return SectionSubjectTeacherCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Room List and Create """


class RoomListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Room
    filterset_class = RoomFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoomListSerializer
        if self.request.method == 'POST':
            return RoomCreateSerializer


""" Room update and Retrive """


class RoomRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Room
    filterset_class = RoomFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoomListSerializer
        if self.request.method == 'PUT':
            return RoomCreateSerializer
        if self.request.method == 'PATCH':
            return RoomCreateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


""" Section List according to Grade """


class SectionListByGrade(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            section_qs = Section.objects.filter(
                grade__id=request.data.get('grade', None))
            section_serializer = SectionListSerializer(section_qs, many=True)
            return Response(section_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Grade list By School """


class GradeListBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def post(self, request):
        try:
            grade_qs = SchoolGradeSubject.objects.filter(
                school__id=request.data.get('school', None))
            grade_serializer = SchoolGradeSubjectSerializer(
                grade_qs, many=True)
            return Response(grade_serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" school according room and subject """


class SubjectAndRoomBySchool(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:

            resultant_dict = {}
            room_qs = Room.objects.filter(school=pk)
            room_serializer = RoomBySchoolSerializer(room_qs, many=True)
            resultant_dict['room_list'] = room_serializer.data
            subject_qs = SchoolGradeSubject.objects.filter(school=pk)
            subject_serializer = SubjectBySchoolSerializer(
                subject_qs, many=True)
            subject_list = subject_serializer.data
            resultant_data = list(zip(*[d.values() for d in subject_list]))
            resultant_data = list(itertools.chain(*resultant_data))
            resultant_data = list(itertools.chain(*resultant_data))
            resultant_dict['subject_list'] = resultant_data
            return Response(resultant_dict, status=status.HTTP_200_OK)

        except Exception as ex:
            print("Error", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Subject list by SectionSubjectTeacher """


class SubjectByAcademicSession(GeneralClass, Mixins, ListCreateAPIView):
    model = AcademicSession
    serializer_class = AcademicSessionListSerializer

    def post(self, request):
        try:
            academic_cal = AcademicCalender.objects.filter(
                pk=request.data.get('academic_calender', None))[0]
            grade = Grade.objects.filter(pk=request.data.get('grade', None))[0]
            section = Section.objects.filter(
                pk=request.data.get('section', None))[0]

            academic_id = AcademicSession.objects.filter(
                academic_calender=academic_cal, grade=grade, section=section)
            print("academic_id-----", academic_id)

            if academic_id:
                academic = academic_id[0]
                subject_qs = SectionSubjectTeacher.objects.filter(
                    academic_session=academic)
                if subject_qs:
                    print("4")
                    subject_qs_serializer = SectionSubjectTeacherListSerializer(
                        subject_qs, many=True)
                    return Response(subject_qs_serializer.data, status=status.HTTP_200_OK)
                else:
                    data = []
                    return Response(data, status=status.HTTP_200_OK)
            else:
                data = []
                return Response("Academic Session is not Avaliable", status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("Error--------", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" session Grade subject class teacher list """


class SessionGradeSectionTeacherSubject(GeneralClass, Mixins, ListCreateAPIView):
    def get(self, request, pk):
        try:
            resultant_dict = {}
            session_qs = AcademicCalender.objects.filter(school=pk)
            session_qs_serializer = AcademicCalenderListSerializer(
                session_qs, many=True)
            resultant_dict['session_list'] = session_qs_serializer.data
            grade_qs = SchoolGradeSubject.objects.filter(school=pk)
            grade_qs_serializer = SchoolGradeListSerializer(
                grade_qs, many=True)
            resultant_dict['grade_list'] = grade_qs_serializer.data
            subject_qs = SchoolGradeSubject.objects.filter(school=pk)
            subject_qs_serializer = SchoolSubjectListSerializer(
                subject_qs, many=True)
            resultant_dict['subject_list'] = subject_qs_serializer.data

            teacher_qs = UserRole.objects.filter(school=pk)
            teacher_qs_serializer = UserRoleListForSchoolSerializer(
                teacher_qs, many=True)
            resultant_dict['teacher_list'] = teacher_qs_serializer.data

            return Response(resultant_dict, status=status.HTTP_200_OK)

        except Exception as ex:
            print("Error", ex)
            logger.debug(ex)
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Bulk Upload Subjects """


class AddSubject(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_subject = []

            for i, f in enumerate(df, start=1):
                f['activity'] = ast.literal_eval(f['activity'])
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    subject_qs = Subject.objects.filter(id=f['id'])[0]
                    subject_qs.name = f['name']
                    subject_qs.type = f['type']
                    subject_qs.activity = f['activity']
                    subject_qs.is_kreedo = f['is_kreedo']
                    subject_qs.is_active = f['is_active']
                    subject_qs.save()
                    added_subject.append(subject_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    subject_qs = Subject.objects.filter(id=f['id'])[0]
                    added_subject.append(subject_qs)
                    subject_qs.delete()
                else:
                    print("Create")

                    subject_serializer = SubjectCreateSerializer(
                        data=dict(f))
                    if subject_serializer.is_valid():
                        subject_serializer.save()
                        added_subject.append(
                            subject_serializer.data)
                        print(subject_serializer.data)
                    else:

                        raise ValidationError(subject_serializer.errors)

            keys = added_subject[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_subject)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            # return Response(path_to_file)
            context = {"isSuccess": True, "message": "Subject Added sucessfully",
                       "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:

            logger.debug(ex)
            # return Response(ex)
            context = {"isSuccess": False, "message": "Issue Subject",
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Bulk Upload GRADE """


class AddGrade(ListCreateAPIView):
    def post(self, request):
        try:
            file_in_memory = request.FILES['file']
            df = pd.read_csv(file_in_memory).to_dict(orient='records')
            added_grade = []

            for i, f in enumerate(df, start=1):
                if not m.isnan(f['id']) and f['isDeleted'] == False:
                    print("UPDATION")
                    grade_qs = Grade.objects.filter(id=f['id'])[0]
                    grade_qs.name = f['name']
                    grade_qs.type = f['type']
                    grade_qs.activity = f['activity']
                    grade_qs.is_active = f['is_active']
                    grade_qs.save()
                    added_grade.append(grade_qs)
                elif not m.isnan(f['id']) and f['isDeleted'] == True:
                    print("DELETION")
                    grade_qs = Grade.objects.filter(id=f['id'])[0]
                    added_grade.append(grade_qs)
                    grade_qs.delete()
                else:
                    print("Create")

                    grade_serializer = GradeSerializer(
                        data=dict(f))
                    if grade_serializer.is_valid():
                        grade_serializer.save()
                        added_grade.append(
                            grade_serializer.data)
                        print(grade_serializer.data)
                    else:

                        raise ValidationError(grade_serializer.errors)

            keys = added_grade[0].keys()
            with open('output.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(added_grade)

            fs = FileStorage()
            fs.bucket.meta.client.upload_file(
                'output.csv', 'kreedo-new', 'files/output.csv')
            path_to_file = 'https://' + \
                str(fs.custom_domain) + '/files/output.csv'
            print(path_to_file)
            context = {
                "isSuccess": True, "message": "Add Grade", "error": "", "data": path_to_file}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            context = {
                "isSuccess": False, "message": "Error on adding grade", "error": "", "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Assigning Account Manager to School."""


class AssignAccountManager(GeneralClass, Mixins, ListCreateAPIView):
    model = School
    serializer_class = AccountManagerAssignSerializer

    def post(self, request):
        try:
            schools = request.data.get("schools", None)
            account_manager = request.data.get('account_manager', None)
            for school_pk in schools:
                data = {
                    'account_manager': account_manager
                }
                school = School.objects.get(pk=school_pk)
                school_serializer = AccountManagerAssignSerializer(
                    school, data=data)
                if school_serializer.is_valid():
                    continue
                context = {"isSuccess": False, "message": "Failed to Assign School to User.",
                           "error": "", "data": None}
                return Response(school_serializer.errors, status=status.HTTP_200_OK)
            else:
                context = {"isSuccess": True, "message": "Schools Assigned Successfully",
                           "error": "", "data": None}
                return Response("Schools Assigned Successfully", status=status.HTTP_200_OK)

        except Exception as ex:
            context = {
                "isSuccess": False, "message": f"{ex}", "error": "", "data": ""}
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""teacher list according to school"""


class TeacherListAccordingToSchool(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = UserRole

    def get(self, request, *args, **kwargs):
        try:
            school = kwargs['pk']
            teacher_list = UserRole.objects.filter(
                school=school,
                role__name='Teacher'
            )
            teachers_data = []
            data = {}
            for teacher in teacher_list:
                user_role_serialzer = TeacherListForSchoolSerializer(teacher)
                data.update({
                    "user_obj": user_role_serialzer.data,
                    "school": teacher.school.id,
                    "role": teacher.role.id
                })
                teachers_data.append(user_role_serialzer.data)
                continue
            return Response(teachers_data)
        except Exception as ex:
            print("error@@", ex)
            return Response(ex)


"""Teacher Subject Association for school"""


class TeacherSubjectAssociation(Mixins, CreateAPIView):
    model = SectionSubjectTeacher

    def post(self, request):
        try:
            academic_session = AcademicSession.objects.filter(
                school=request.data.get('school', None),
                grade=request.data.get('grade', None),
                section=request.data.get('section', None),
                academic_calender=request.data.get('academic_calendar', None)
            )
            if academic_session:
                academic_sess = academic_session[0]
                academic_sess.class_teacher = UserDetail.objects.get(
                    user_obj__id=request.data.get('class_teacher'))
                academic_session[0].save()
                section_subject_teacher_list = request.data.get(
                    'subjectsAssociatedTeachers', None)
                for record in section_subject_teacher_list:
                    record['academic_session'] = academic_sess.id
                section_subject_teacher_serializer = SectionSubjectTeacherCreateSerializer(
                    data=section_subject_teacher_list, many=True)
                if section_subject_teacher_serializer.is_valid():
                    section_subject_teacher_serializer.save()
                    context = {
                        "isSuccess": True, "status": 200, "message": "Associate added successfully",
                        "data": section_subject_teacher_serializer.data
                    }
                    return Response(context)
                context = {
                    "isSuccess": False, "status": 200, "message": "Associate section error",
                    "data": section_subject_teacher_serializer.errors
                }
                return Response(context)
            else:
                context = {
                    "isSuccess": False, "status": 200, "message": "Academic Session Not Found",
                    "data": None
                }
                return Response(context)

        except Exception as ex:
            print("error@@", ex)
            context = {
                "isSuccess": False, "status": 500, "message": f"{ex}",
                "data": None
            }
            return Response(context)


""" update teacher-subject based on """


class UpdateTeacherSubjectAssociation(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
    model = SectionSubjectTeacher

    def put(self, request):
        try:
            response_data = []
            academic_session = AcademicSession.objects.get(
                pk=request.data.get('academic_session'))
            academic_data = {
                'section': request.data.get('section', None),
                'grade': request.data.get('grade', None),
                'academic_calender': request.data.get('academic_calendar', None),
                'class_teacher': request.data.get('class_teacher', None)
            }
            academic_session_serializer = AcademicSessionUpdateSerializer(
                academic_session, data=academic_data)

            if academic_session_serializer.is_valid():
                academic_session_serializer.save()

                response_data.append(academic_session_serializer.data)
                response_data[0]['subject_teacher_list'] = []

            else:
                return Response(academic_session_serializer.errors)
            subject_teacher_list = request.data.get(
                'subjectsAssociatedTeachers', None)

            for record in subject_teacher_list:
                print('id', record['id'])
                record['academic_session'] = academic_session.id
                if record['id'] or (record['id'] == None and SectionSubjectTeacher.objects.filter(subject=record['subject'], academic_session=record['academic_session'])):
                    if record['id']:
                        subject_teacher_obj = SectionSubjectTeacher.objects.get(
                            pk=record['id'])
                    else:
                        subject_teacher_obj = SectionSubjectTeacher.objects.get(
                            subject=record['subject'], academic_session=record['academic_session'])
                    subject_teacher_serializer = SectionSubjectTeacherCreateSerializer(
                        subject_teacher_obj, data=record)
                    if subject_teacher_serializer.is_valid():
                        subject_teacher_serializer.save()
                        response_data[0]['subject_teacher_list'].append(
                            subject_teacher_serializer.data)
                        continue
                    else:
                        return Response(subject_teacher_serializer.errors)
                else:

                    subject_teacher_serializer = SectionSubjectTeacherCreateSerializer(
                        data=record)
                    if subject_teacher_serializer.is_valid():
                        subject_teacher_serializer.save()
                        response_data[0]['subject_teacher_list'].append(
                            subject_teacher_serializer.data)
                        continue
                    else:
                        return Response(subject_teacher_serializer.errors)

            deleted_subject_teacher_list = request.data.get(
                'deletedSubjectsAssociatedTeachers', None)
            for record in deleted_subject_teacher_list:
                subject_teacher_obj = SectionSubjectTeacher.objects.get(
                    pk=record['id'])
                subject_teacher_obj.delete()
                print('object deleted')
            return Response(response_data)
        except Exception as ex:
            print("error@@", ex)
            return Response(ex)


"""alter subject list in associate section"""


class AlterSubjectList(GeneralClass, Mixins, ListCreateAPIView):
    model = SectionSubjectTeacher

    def post(self, request):
        try:
            response_data = []
            academic_session = AcademicSession.objects.get(
                pk=request.data.get('academic_session'))
            subject_list = request.data.get('addedSubjects', None)
            for record in subject_list:
                record['academic_session'] = academic_session.id
                if record['id']:
                    print("update", record)
                    subject_teacher_obj = SectionSubjectTeacher.objects.get(
                        pk=record['id'])
                    subject_teacher_serializer = SectionSubjectTeacherCreateSerializer(
                        subject_teacher_obj, data=record)
                    if subject_teacher_serializer.is_valid():
                        subject_teacher_serializer.save()
                        response_data.append(subject_teacher_serializer.data)
                        continue
                    else:
                        return Response(subject_teacher_serializer.errors)
                else:
                    print("create", record)
                    subject_teacher_serializer = SectionSubjectTeacherCreateSerializer(
                        data=record)
                    if subject_teacher_serializer.is_valid():
                        subject_teacher_serializer.save()
                        response_data.append(subject_teacher_serializer.data)
                        continue
                    else:
                        return Response(subject_teacher_serializer.errors)

            deletedSubjects = request.data.get('deletedSubjects', None)
            for record in deletedSubjects:
                subject_teacher_obj = SectionSubjectTeacher.objects.get(
                    pk=record['id'])
                subject_teacher_obj.delete()
                print('object deleted')
            return Response(response_data)

        except Exception as ex:
            print("error@@", ex)
            return Response(ex)
