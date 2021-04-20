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
]
