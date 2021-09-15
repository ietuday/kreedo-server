from django.urls import path, re_path
from .views import*


urlpatterns = [

    path('holiday_type_list',
         HolidayTypeListCreate.as_view(), name='HolidayTypeListCreate'),

    path('school_holiday_list_by_school/<int:pk>', SchoolHolidayListBySchool.as_view(),
         name='SchoolHolidayListBySchool'),

    path('school_holiday_list_create',
         SchoolHolidayListCreate.as_view(), name='SchoolHolidayListCreate'),

    path('create_school_holiday',
         CreateSchoolHoliday.as_view(), name='CreateSchoolHoliday'),

    path('school_holiday_retrive_update_delete/<int:pk>', SchoolHolidayRetriveUpdateDestroy.as_view(),
         name='SchoolHolidayRetriveUpdateDestroy'),

    path('update_school_holiday/<int:pk>', UpdateSchoolHoliday.as_view(),
         name='UpdateSchoolHoliday'),


    path('school_weak_off_list_create',
         SchoolWeakOffListCreate.as_view(), name='SchoolWeakOffListCreate'),
    path('school_weak_off_retrive_update_delete/<int:pk>', SchoolWeakOffRetriveUpdateDestroy.as_view(),
         name='SchoolWeakOffRetriveUpdateDestroy'),
    path('calendar', Calendar.as_view(), name='Calendar'),
    path('holiday_list_by_date_and_type',
         HolidayListByType.as_view(), name='HolidayListByType'),

    #     path('week_off_by_academic_session/<int:pk>', SchoolWeakOffByAcademicSession.as_view(),
    #          name='SchoolWeakOffByAcademicSession'),

    path('week_off_by_academic_calender/<int:pk>', WeekOffByAcademicCalender.as_view(),
         name='WeekOffByAcademicCalender'),

    path('week_off_by_academic_session/<int:pk>', WeekOffByAcademicSession.as_view(),
         name='WeekOffByAcademicSession'),


    path('holiday_list_by_academic_session/<int:pk>', HolidayListByAcademicSession.as_view(),
         name='HolidayListByAcademicSession'),

    path('holiday_list_of_month_by_school',
         HolidayListOfMonthBySchool.as_view(), name='HolidayListOfMonthBySchool'),
    path('holiday_list_of_month_by_academic_session',
         HolidayListOfMonthByAcademicSession.as_view(), name='HolidayListOfMonthByAcademicSession'),
    path('download_list_of_holiday_in_csv_by_school', DownloadListOfHolidaysInCSVBySchool.as_view(),
         name='DownloadListOfHolidaysInCSVBySchool'),

    path('holiday_list_of_month_by_academic_calender', HolidayListOfMonthByAcademicCalender.as_view(),
         name='HolidayListOfMonthByAcademicCalender'),




]
