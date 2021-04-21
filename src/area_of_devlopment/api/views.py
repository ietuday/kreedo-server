from django.shortcuts import render


from .serializer import*
from area_of_devlopment.models import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from .filters import*

# Create your views here.


""" Area of Devlopment List and Create """


class AreaOfDevlopmentListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = AreaOfDevlopment
    filterset_class = AreaOfDevlopmentFilter
    serializer_class = AreaOfDevlopmentSerializer


""" Area of Devlopment Update and Delete """


class AreaOfDevlopmentRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = AreaOfDevlopment
    filterset_class = AreaOfDevlopmentFilter
    serializer_class = AreaOfDevlopmentSerializer


""" Concept List and Create """


class ConceptListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Concept
    filterset_class = ConceptFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConceptListSerializer
        if self.request.method == 'POST':
            return ConceptCreateSerializer


""" Retrive update and delete Concept """


class ConceptRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Concept
    filterset_class = ConceptFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConceptListSerializer
        if self.request.method == 'PUT':
            return ConceptCreateSerializer
        if self.request.method == 'DELETE':
            return ConceptListSerializer


""" Skill List and Create """


class SkillListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Skill
    filterset_class = SkillFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SkillListSerializer
        if self.request.method == 'POST':
            return SkillCreateSerializer


""" Skill Update And Retrive """


class SkillRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Skill
    filterset_class = SkillFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SkillListSerializer
        if self.request.method == 'PUT':
            return SkillCreateSerializer
        if self.request.method == 'DELETE':
            return SkillListSerializer
