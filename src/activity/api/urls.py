from django.urls import path
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
    path('activity-complete_list_create',
         ActivityCompleteListCreate.as_view(), name='ActivityCompleteListCreate'),
    path('activity-complete_retrive_update_delete/<int:pk>', ActivityCompleteRetriveUpdateDestroy.as_view(),
         name='ActivityCompleteRetriveUpdateDestroy'),
     path('activity-complete_retrive_update_delete', ActivityCompleteRetriveUpdateDestroy.as_view(),
         name='ActivityCompleteRetriveUpdateDestroy'),
]
