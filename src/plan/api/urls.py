from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('plan_list_create',
         PlanListCreate.as_view(), name='PlanListCreate'),
    path('plan_retrive_update_delete/<int:pk>', PlanRetriveUpdateDelete.as_view(),
         name='PlanRetriveUpdateDelete'),
    path('child-plan_list_create',
         ChildPlanListCreate.as_view(), name='ChildPlanListCreate'),
    path('child-plan_retrive_update_delete/<int:pk>', ChildPlanRetriveUpdateDelete.as_view(),
         name='ChildPlanRetriveUpdateDelete'),
    path('plan-activity_list_create',
         PlanActivityListCreate.as_view(), name='PlanActivityListCreate'),
    path('plan-activity_retrive_update_delete/<int:pk>', PlanActivityRetriveUpdateDestroy.as_view(),
         name='PlanActivityRetriveUpdateDestroy'),


    path('subject-school-grade-plan_list_create',
         SubjectSchoolGradePlanListCreate.as_view(), name='SubjectSchoolGradePlanListCreate'),
    path('subject-school-grade-plan_retrive_update_delete/<int:pk>', SubjectSchoolGradePlanRetriveUpdateDestroy.as_view(),
         name='SubjectSchoolGradePlanRetriveUpdateDestroy'),

]
