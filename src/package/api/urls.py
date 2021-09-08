from .views import*
from django.urls import path, re_path


urlpatterns = [
    path('package_list_create', PackageListCreate.as_view(),
         name='PackageListCreate'),
    path('package_retrive_update_delete/<int:pk>', PackageRetriveUpdateDestroy.as_view(),
         name='PackageRetriveUpdateDestroy'),
    path('school-package_list_create', SchoolPackageListCreate.as_view(),
         name='SchoolPackageListCreate'),
    path('school-package_retrive_update_delete/<int:pk>', SchoolPackageRetriveUpdateDelete.as_view(),
         name='SchoolPackageRetriveUpdateDelete'),
    path('material_list_by_package/<int:pk>', MaterialListByPackage.as_view(),
         name='MaterialListByPackage'),

    path('bulk-upload/add-package',
         AddPackage.as_view(), name='AddPackage'),



]
