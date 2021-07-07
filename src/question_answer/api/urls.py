from django.urls import path
from .views import*


urlpatterns = [

    path('secret_question_answer_list_create',SecretQuestionAnswerListCreate.as_view(), name='SecretQuestionAnswerListCreate'),
    # path()
]