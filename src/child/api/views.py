from django.shortcuts import render
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from kreedo.general_views import*
from child.models import*
from .filters import*
from .serializer import*

# Create your views here.

""" create and List Child """


class ChildListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Child
    filterset_class = ChildFilter
