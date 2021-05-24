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
     path('activity_list_by_child', ActivityListByChild.as_view(), name='ActivityListByChild'),


    path('activity-detail_retrive_by_child/<int:pk>', ActivityDetail.as_view(),
         name='ActivityDetail'),

     
     
]
