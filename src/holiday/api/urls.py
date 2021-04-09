from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('school-holiday_list_create',
         SchoolHolidayListCreate.as_view(), name='SchoolHolidayListCreate'),
    path('school-holiday_retrive_update_delete/<int:pk>', SchoolHolidayRetriveUpdateDestroy.as_view(),
         name='SchoolHolidayRetriveUpdateDestroy'),
    path('school-weak-off_list_create',
         SchoolWeakOffListCreate.as_view(), name='SchoolWeakOffListCreate'),
    path('school-weak-off_retrive_update_delete/<int:pk>', SchoolWeakOffRetriveUpdateDestroy.as_view(),
         name='SchoolWeakOffRetriveUpdateDestroy'),



]
