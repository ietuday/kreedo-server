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

# Create your views here.

""" create and List Child """


class ChildListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Child
    filterset_class = ChildFilter
    serializer_class = ChildCreateSerializer

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
                # print("Context", context)
                child_detail_serializer = ChildCreateSerializer(
                    data=dict(child_detail), context=context)
                if child_detail_serializer.is_valid():
                    child_detail_serializer.save()
                    print("child", child_detail_serializer.data)
                    return Response(child_detail_serializer.data)
                else:
                    print("child error",  child_detail_serializer.errors)
                    return Response(child_detail_serializer.errors)

            except Exception as ex:
                print("error", ex)
                print("traceback", traceback.print_exc())
                return Response(ex)

        except Exception as ex:
            print("ex", ex)
            return Response(ex)


""" Child list  """


class ChildList(GeneralClass, Mixins, ListAPIView):
    model = Child
    serializer_class = ChildListSerializer


""" Update Child """


class ChildListCreate(GeneralClass, Mixins, CreateAPIView):
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
