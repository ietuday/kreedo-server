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


class SecretQuestionAnswerListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = QuestionAnswer
    filterset_class = QuestionAnswerFilter
    serializer_class = QuestionAnswerSerializer


""" Secret Question and answer Retrive, Update and Delete """


class SecretQuestionAnswerRetriveUpdateDelete(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = QuestionAnswer
    filterset_class = QuestionAnswerFilter
    serializer_class = QuestionAnswerSerializer


""" Get Random Questions """


class RandomQuestion(ListCreateAPIView):
    def get(self, request):
        try:
            #  count, random number
            items = list(QuestionAnswer.objects.all())
            question = random.sample(items, 1)
            question_serializer = QuestionSerializer(question)

            context = {'isSuccess': True, "error": "",
                       "statusCode": status.HTTP_200_OK, 'data': question_serializer.data}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Valiodate Answer """


class ValidateAnswer(ListCreateAPIView):
    def post(self, request):
        try:
            if QuestionAnswer.objects.filter(id=request.data.get('id', None), answer=request.data.get('answer', None)).exists():
                context = {'isSuccess': True, "error": "",
                           "statusCode": status.HTTP_200_OK, 'data': "Answer is Correct"}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {'isSuccess': False, "error": "",
                           "statusCode": status.HTTP_200_OK, 'data': "Answer is InCorrect"}
                return Response(context, status=status.HTTP_200_OK)

        except Exception as ex:
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





""" GetSecretQuestionBasedOnParentID """
class GetSecretQuestionBasedOnParentID(ListCreateAPIView):
    def get(self, request, pk):
        try:
            question_answer = QuestionAnswer.objects.filter(user=pk)
            
            
            if len(question_answer) !=0:
                user_qs = User.objects.get(id=pk)
            
                user_detail = {
                    "user":user_qs.id,
                    "email":user_qs.email
                    }
                context = super().get_serializer_context()
                context.update({"user_detail": user_detail})
                question_answer_serializer = GetSecretQuestionBasedOnParentIDSerializer(question_answer,context=context, many=True)
                # return Response(question_answer_serializer.data)
                context = {'isSuccess': True, "error": "",
                           "statusCode": status.HTTP_200_OK, 'data':question_answer_serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                
                context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            print(ex)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" UpdateSecretQuestionBasedOnParentID """
class UpdateSecretQuestionBasedOnParentID(ListCreateAPIView):
    def put(self, request, pk):
        try:
            question_answer = QuestionAnswer.objects.filter(user=pk)
            print(question_answer)
           
           
        except Exception as ex:
            print(ex)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" ValidateSecretQuestionForParentEmailID """
class ValidateSecretQuestionForParentEmailID(ListCreateAPIView):
    def post(self, request):
        try:
            if User.objects.filter(email=request.data.get('email',None)).exists():
                user_qs = User.objects.get(email=request.data.get('email',None))
    
                if QuestionAnswer.objects.filter(user=user_qs.id, question=request.data.get('question',None)).exists():
                    context = {'isSuccess': True, "error": "",'message':"True",
                           "statusCode": status.HTTP_200_OK, 'data':"True"}
                    return Response(context, status=status.HTTP_200_OK) 
                else:

                    context = {'isSuccess': False, 'message': "False",
                                    'data': "False", "statusCode": status.HTTP_404_NOT_FOUND}
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            else:
            

                context = {'isSuccess': True, 'message': "User EmailId Not found",
                                'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print(ex)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




""" ValidateSecretQuestionForParentID """
class ValidateSecretQuestionForParentID(ListCreateAPIView):
    def post(self, request):
        try:
            if User.objects.filter(id=request.data.get('parent_id',None)).exists():
                user_qs = User.objects.get(id=request.data.get('parent_id',None))
    
                if QuestionAnswer.objects.filter(user=user_qs.id, question=request.data.get('question',None)).exists():
                    context = {'isSuccess': True, "error": "",'message':"True",
                           "statusCode": status.HTTP_200_OK, 'data':"True"}
                    return Response(context, status=status.HTTP_200_OK) 
                else:

                    context = {'isSuccess': False, 'message': "False",
                                    'data': "False", "statusCode": status.HTTP_404_NOT_FOUND}
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            else:
    
                context = {'isSuccess': True, 'message': "User Id Not found",
                                'data': "", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print(ex)
            context = {'isSuccess': False, "error": ex,
                       "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, 'data': ''}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
