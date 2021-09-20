from django.urls import path, re_path
from .views import*
from .edoofun_views import*

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
    path('subject_school_grade_plan_list_create',
         SubjectSchoolGradePlanListCreate.as_view(), name='SubjectSchoolGradePlanListCreate'),
    path('subject_school_grade_plan_retrive_update_delete/<int:pk>', SubjectSchoolGradePlanRetriveUpdateDestroy.as_view(),
         name='SubjectSchoolGradePlanRetriveUpdateDestroy'),
    path('child-activity',
         ChildActivity.as_view(), name='ChildActivity'),
    path('grade_subject_list_by_school/<int:pk>',
         GradeSubjectListBySchool.as_view(), name='GradeSubjectListBySchool'),
    path('add_subject_by_grade',
         AddSubjectByGrade.as_view(), name='AddSubjectByGrade'),
    path('grades_by_school/<int:pk>',
         GradesBySchool.as_view(), name='GradesBySchool'),
    path('create_subject_by_school',
         SubjectSchoolPlanListCreate.as_view(), name='SubjectSchoolPlanListCreate'),

    path('bulk-upload/add-plan',
         AddPlan.as_view(), name='AddPlan'),


    path('edoofun/get_child_list_associated_to_section_id',
         GetChildListAssociatedToSectionID.as_view(), name='get child List By section'),

]
