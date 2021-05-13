from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('material_list_create',
         MaterialListCreate.as_view(), name='MaterialListCreate'),
    path('material_retrive_update_delete/<int:pk>', MaterialRetriveUpdateDestroy.as_view(),
         name='MaterialRetriveUpdateDestroy'),

    path('activity-master-supporting-material_list_create',
         ActivityMasterSupportingMaterialListCreate.as_view(), name='ActivityMasterSupportingMaterialListCreate'),

    path('bulk-upload/add-material',
         AddMaterial.as_view(), name='Add Material'),




]
