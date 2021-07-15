from django.urls import path
from .views import*


urlpatterns = [

    path('secret_question_answer_list_create',SecretQuestionAnswerListCreate.as_view(), name='SecretQuestionAnswerListCreate'),
    path('secret_question_answer_retrive_update_delete/<int:pk>', SecretQuestionAnswerRetriveUpdateDelete.as_view(),
         name='SecretQuestionAnswerRetriveUpdateDelete'),
    path('get_random_question',RandomQuestion.as_view(), 
        name='RandomQuestion'),
    path('validate_answer',ValidateAnswer.as_view(), 
        name='ValidateAnswer'),


]