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
from rest_framework import status
# Create your views here.

""" create and List Child """


class ChildListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Child
    serializer_class = ChildListSerializer

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
            print("ex", ex)
            return Response(ex)


""" Child list  """


class ChildList(GeneralClass, Mixins, ListAPIView):
    model = Child
    serializer_class = ChildListSerializer


""" Update Child """


class ChildDetailListCreate(GeneralClass, Mixins, CreateAPIView):
    model = ChildDetail

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildDetailListSerializer

        if self.request.method == 'POST':
            return ChildDetailCreateSerializer


class ChildRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = ChildDetail

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChildDetailListSerializer

        if self.request.method == 'PUT':
            return ChildDetailCreateSerializer

        if self.request.method == 'DELETE':
            return ChildDetailListSerializer


""" Attendance List and Create """


class AttendanceListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Attendance

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AttendanceListSerializer

        if self.request.method == 'POST':
            return AttendanceCreateSerializer


""" Attendance Retrive Update and Delete """


class AttendanceRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Attendance

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AttendanceListSerializer

        if self.request.method == 'PUT':
            return AttendanceCreateSerializer

        if self.request.method == 'DELETE':
            return AttendanceListSerializer


""" child List of class, section and subject """


class childListAccordingToClass(ListCreateAPIView):
    def post(self, request):
        try:
            grade = request.data.get('grade', None)
            section = request.data.get('section', None)
            subject = request.data.get('subject', None)
            academic_id = AcademicSession.objects.get(
                grade__name=grade, section__name=section).id
            subject = Subject.objects.get(name=subject).name

            child_query = ChildPlan.objects.filter(
                academic_session=academic_id, subjects__name=subject)
            child_serailizer = ChildPlanListSerializer(child_query, many=True)

            context = {"message": "Child List According to grade",
                       "data": child_serailizer.data, "statusCode": status.HTTP_200_OK}
            return Response(context)

        except Exception as ex:
            
            logger.info(ex)
            logger.debug(ex)
            return Response(ex)


class AttendenceByAcademicSession(ListCreateAPIView):
    def post(self, request):
        try:
            grade = request.data.get('grade', None)
            section = request.data.get('section', None)
            attendance_date = request.data.get('attendance_date', None)
            academic_id = AcademicSession.objects.get(
                grade=grade, section=section).id

            attendence_qs = Attendance.objects.filter(academic_session=academic_id,attendance_date= attendance_date)
            attendanceListSerializer = AttendanceListSerializer(attendence_qs, many=True)
            context = {"message": "Attendence By Academic Session",
                       "data": attendanceListSerializer.data, "statusCode": status.HTTP_200_OK}
            return Response(context)

        except Exception as ex:
            print("Eror", ex)
            logger.info(ex)
            logger.debug(ex)
            return Response(ex)
