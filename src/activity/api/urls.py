from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('activity_list_create',
         ActivityListCreate.as_view(), name='ActivityListCreate'),
    path('activity_retrive_update_delete/<int:pk>', ActivityRetriveUpdateDestroy.as_view(),
         name='ActivityRetriveUpdateDestroy'),

    path('activity-asset_list_create',
         ActivityAssetListCreate.as_view(), name='ActivityAssetListCreate'),
    path('activity-asset_retrive_update_delete/<int:pk>', ActivityAssetRetriveUpdateDestroy.as_view(),
         name='ActivityAssetRetriveUpdateDestroy'),
    path('group-activity-missed_list_create',
         GroupActivityMissedListCreate.as_view(), name='GroupActivityMissedListCreate'),
    path('group-activity-missed_retrive_update_delete/<int:pk>', GroupActivityMissedRetriveUpdateDestroy.as_view(),
         name='GroupActivityMissedRetriveUpdateDestroy'),
]
