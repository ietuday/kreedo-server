from django.urls import path
from .views import*


urlpatterns = [
    path('activity_list_create',
         ActivityListCreate.as_view(), name='ActivityListCreate'),
    path('activity_list_by_subject/<int:subject>/<int:child>',
         ActivityListBySubject.as_view(), name='ActivityListBySubject'), 
     path('activity_list_by_subject_web/<int:subject>',
         ActivityListBySubjectWeb.as_view(), name='ActivityListBySubject'), 
    path('activity_retrive_update_delete/<int:pk>', ActivityRetriveUpdateDestroy.as_view(),
         name='ActivityRetriveUpdateDestroy'),
    path('activity-asset_list_create',
         ActivityAssetListCreate.as_view(), name='ActivityAssetListCreate'),
    path('activity-asset_retrive_update_delete/<int:pk>', ActivityAssetRetriveUpdateDestroy.as_view(),
         name='ActivityAssetRetriveUpdateDestroy'),
    path('activity-complete_list_create',
         ActivityCompleteListCreate.as_view(), name='ActivityCompleteListCreate'),
    path('activity-complete_retrive_update_delete/<int:pk>', ActivityCompleteRetriveUpdateDestroy.as_view(),
         name='ActivityCompleteRetriveUpdateDestroy'),
     path('activity-complete_retrive_update_delete', ActivityCompleteRetriveUpdateDestroy.as_view(),
         name='ActivityCompleteRetriveUpdateDestroy'),
     path('bulk-upload/add-activity',
         AddActivity.as_view(), name='AddActivity'),
     path('activity-complete_list_create_mob',
         ActivityCompleteListCreateMob.as_view(), name='ActivityCompleteListCreateMob'),

     path('bulk-upload/add-activity-assets',
         AddActivityAsset.as_view(), name='AddActivityAsset'),
     path('activity-complete_list_create_group',
         ActivityCompleteListCreateGroup.as_view(), name='ActivityCompleteListCreateGroup'),

]
