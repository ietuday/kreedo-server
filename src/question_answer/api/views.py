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
import random
# Create your views here.



""" Secret Question and answer list create """

class SecretQuestionAnswerListCreate(GeneralClass,Mixins,ListCreateAPIView):
    model = QuestionAnswer
    filterset_class = QuestionAnswerFilter
    serializer_class = QuestionAnswerSerializer

""" Secret Question and answer Retrive, Update and Delete """

class SecretQuestionAnswerRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = QuestionAnswer
    filterset_class = QuestionAnswerFilter
    serializer_class = QuestionAnswerSerializer


""" Get Random Questions """
import random
class RandomQuestion(ListCreateAPIView):
    def get(self, request):
        try:
            items = list(QuestionAnswer.objects.all())
            question =  random.sample(items,1)
            question_serializer = QuestionSerializer(question, many=True)
           
            context = {'isSuccess': True, "error": "",
                        "statusCode": status.HTTP_200_OK,'data':question_serializer.data}
            return Response(context,status=status.HTTP_200_OK)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         

""" Valiodate Answer """
class ValidateAnswer(ListCreateAPIView):
    def post(self, request):
        try:
            if QuestionAnswer.objects.filter(id=request.data.get('id', None),answer=request.data.get('answer', None)).exists():
                context = {'isSuccess': True, "error": "",
                        "statusCode": status.HTTP_200_OK,'data':"Answer is Correct"}
                return Response(context,status=status.HTTP_200_OK)  
            else:
                context = {'isSuccess': False, "error": "",
                            "statusCode": status.HTTP_200_OK,'data':"Answer is InCorrect"}
                return Response(context,status=status.HTTP_200_OK)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,'data':''}
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         