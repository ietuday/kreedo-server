from django.urls import path, re_path
from .views import*


urlpatterns = [

     path('holiday_type_list',
         HolidayTypeListCreate.as_view(), name='HolidayTypeListCreate'),
     
     path('school-holiday_list_by_school/<int:pk>', SchoolHolidayListBySchool.as_view(),
          name='SchoolHolidayListBySchool'),

     path('school-holiday_list_create',
          SchoolHolidayListCreate.as_view(), name='SchoolHolidayListCreate'),
     path('school-holiday_retrive_update_delete/<int:pk>', SchoolHolidayRetriveUpdateDestroy.as_view(),
          name='SchoolHolidayRetriveUpdateDestroy'),
     path('school-weak-off_list_create',
          SchoolWeakOffListCreate.as_view(), name='SchoolWeakOffListCreate'),
     path('school-weak-off_retrive_update_delete/<int:pk>', SchoolWeakOffRetriveUpdateDestroy.as_view(),
          name='SchoolWeakOffRetriveUpdateDestroy'),
     path('calendar', Calendar.as_view(), name='Calendar'),
     path('holiday_list_by_date_and_type', HolidayListByType.as_view(), name='HolidayListByType')




]
