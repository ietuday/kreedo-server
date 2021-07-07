from django.shortcuts import render
from .serializer import*
from kreedo.general_views import *
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from kreedo.conf.logger import CustomFormatter
import logging
from rest_framework import status
from ..models import*
from .filters import*

# Create your views here.

class SecretQuestionAnswerListCreate(GeneralClass,Mixins,ListCreateAPIView):
    model = QuestionAnswer
    filterset_class = QuestionAnswerFilter
    serializer_class = QuestionAnswerSerializer


class SecretQuestionAnswerRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = QuestionAnswer
    filterset_class = QuestionAnswerFilter
    serializer_class = QuestionAnswerSerializer



