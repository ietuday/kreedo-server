from django.shortcuts import render

"""
    REST LIBRARY IMPORT
"""

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView

"""
    IMPORT CORE FILES 
"""
from  kreedo.general_views import Mixins,GeneralClass

"""
    IMPORT USER APP FILE
""" 
from .serializer import*
from  ..models import*
from .filters import*


# Create your views here.

class RoleListCreate(Mixins,GeneralClass,ListCreateAPIView):
    model = Role
    serializer_class = RoleSerializer
    filterset_class = RoleFilter


class RoleRetriveUpdateDestroy(Mixins,GeneralClass,RetrieveUpdateDestroyAPIView):
    model = Role
    serializer_class = RoleSerializer
    filterset_class = RoleFilter




