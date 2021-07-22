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
    path('get_secret_question_based_on_parent_id/<int:pk>', GetSecretQuestionBasedOnParentID.as_view(),
         name='GetSecretQuestionBasedOnParentID'),
    
    path('updatet_secret_question_based_on_parent_id/<int:pk>', UpdateSecretQuestionBasedOnParentID.as_view(),
         name='UpdateSecretQuestionBasedOnParentID'),

    path('validate_secret_question_for_parent_emailid',ValidateSecretQuestionForParentEmailID.as_view(), 
        name='ValidateSecretQuestionForParentEmailID'),

    path('validate_secret_question_for_parent_id',ValidateSecretQuestionForParentID.as_view(), 
        name='ValidateSecretQuestionForParentID'),



]