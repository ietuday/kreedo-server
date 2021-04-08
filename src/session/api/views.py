from django.shortcuts import render
"""
    REST LIBRARY IMPORT
"""
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
                                        
from rest_framework.response import Response

"""
    IMPORT CORE FILES 
"""
from kreedo.general_views import *

"""
    IMPORT USER APP FILE
"""
from schools.models import*
from .serializer import*
from .filters import *
# Create your views here.

""" School Session Create  and list """
class SchoolSessionListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = SchoolSession
    serializer_class = SchoolSessionSerializer
    filterset_class = SchoolSessionFilter

  
""" School Session Retrive Update Delete """
class SchoolSessionRetriveUpdateDestroy(GeneralClass,Mixins,RetrieveUpdateDestroyAPIView):
    model = SchoolSession
    serializer_class = SchoolSessionSerializer
    filterset_class = SchoolSessionFilter
