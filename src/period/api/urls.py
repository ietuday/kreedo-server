from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('period-template_list_create',
         PeriodTemplateListCreate.as_view(), name='PeriodTemplateListCreate'),
    path('period-template_retrive_update_delete/<int:pk>', PeriodTemplateRetriveUpdateDestroy.as_view(),
         name='PeriodTemplateRetriveUpdateDestroy'),

    path('period-template-detail_list_create',
         PeriodTemplateDetailListCreate.as_view(), name='PeriodTemplateDetailListCreate'),

    path('period-template-detail_retrive_update_delete/<int:pk>', PeriodTemplateDetailRetriveUpdateDestroy.as_view(),
         name='PeriodTemplateDetailRetriveUpdateDestroy'),

    path('period_list_create',
         PeriodListCreate.as_view(), name='PeriodListCreate'),


    path('period_retrive_update_delete/<int:pk>', PeriodRetriveUpdateDestroy.as_view(),
         name='PeriodRetriveUpdateDestroy'),

    path('classes_by_teacher_list',
         ClassAccordingToTeacher.as_view(), name='ClassAccordingToTeacher'),

    path('activity_by_child', ActivityByChild.as_view(), name='ActivityByChild'),
    path('activity_list_by_child', ActivityListByChild.as_view(),
         name='ActivityListByChild'),


    path('activity-detail_retrive_by_child/<int:pk>', ActivityDetail.as_view(),
         name='ActivityDetail'),
    path('period_template_apply_to_grade', PeriodTemplateAppyToGradesListCreate.as_view(),
         name='PeriodTemplateAppyToGradesListCreate'),


    path('period_template_apply_to_grade_retrive_update_delete/<int:pk>', PeriodTemplateAppyToGradesRetriveUpdateDestroy.as_view(),
         name='PeriodTemplateAppyToGradesRetriveUpdateDestroy'),
    path('period_create',
         PeriodCreate.as_view(), name='PeriodCreate'),
    path('period_month_list',
         PeriodMonthList.as_view(), name='PeriodMonthList'),
    path('period_list_according_to_date',
         PerioListAccordingDate.as_view(), name='PerioListAccordingDate'),
    path('period_template_detail_by_period_template/<int:pk>', PeriodTemplateDetailByPeriodTemplate.as_view(),
         name='PeriodTemplateDetailByPeriodTemplate'),
    path('get_period_count_by_academic_session',
         PeriodCountListByAcademicSession.as_view(), name='PeriodCountListByAcademicSession'),



]
