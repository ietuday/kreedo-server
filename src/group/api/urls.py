from django.urls import path
from .views import*


urlpatterns = [
    path('group_list_create',
         GroupListCreate.as_view(), name='GroupListCreate'),

    path('group_retrive_update_delete/<int:pk>', GroupRetriveUpdateDelete.as_view(),
         name='GroupRetriveUpdateDelete'),
         
     path('permission_list_create',
         PermissionListCreate.as_view(), name='PermissionListCreate'),
     path('permission_retrive_update_delete/<int:pk>', PermissionRetriveUpdateDelete.as_view(),
         name='PermissionRetriveUpdateDelete'),
     

]