from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('subject-school-grade-plan_list_create',
         SubjectSchoolGradePlanListCreate.as_view(), name='SubjectSchoolGradePlanListCreate'),
    path('subject-school-grade-plan_retrive_update_delete/<int:pk>', SubjectSchoolGradePlanRetriveUpdateDestroy.as_view(),
         name='SubjectSchoolGradePlanRetriveUpdateDestroy'),

]
