from django.urls import path, re_path
from .views import*
from .edoofun_views import*

urlpatterns = [
    path('school_session_list_create', SchoolSessionListCreate.as_view(),
         name='SchoolSessionListCreate'),
    path('school_session_retrive_update_delete/<int:pk>', SchoolSessionRetriveUpdateDestroy.as_view(),
         name='SchoolSessionRetriveUpdateDestroy'),
    path('academic_session_list_create', AcademicSessionListCreate.as_view(),
         name='AcademicSessionListCreate'),
    path('academic_session_retrive_update_delete/<int:pk>', AcademicSessionRetriveUpdateDestroy.as_view(),
         name='AcademicSessionRetriveUpdateDestroy'),
    path('academic_calender_list_create', AcademicCalenderListCreate.as_view(),
         name='AcademicCalenderListCreate'),
    path('academic_calender_retrive_update_delete/<int:pk>', AcademicCalenderRetriveUpdateDestroy.as_view(),
         name='AcademicCalenderRetriveUpdateDestroy'),
    path('academic_session_by_teacher', AcademicSessionByTeacher.as_view(),
         name='AcademicSessionByTeacher'),
    path('generate_calender_to_pdf/<int:pk>', GenerateCalenderToPdf.as_view(),
         name='GenerateCalenderToPdf'),
    path('academic_session_by_school', AcademicSessionBySchool.as_view(),
         name='AcademicSessionBySchool'),
    path('academic_calender_list_by_school/<int:pk>', AcademicCalenderListBySchool.as_view(),
         name='AcademicCalenderListBySchool'),
    path('grade_and_section_list_by_school', GradeAndSectionListBySchool.as_view(),
         name='GradeAndSectionListBySchool'),
    path('apply_academic_calender_to_academic_session/<int:pk>', ApplyAcademicCalenderToAcademicSession.as_view(),
         name='ApplyAcademicCalenderToAcademicSession'),
    path('academic_calender_by_school/<int:pk>', AcademicCalenderBySchool.as_view(),
         name='AcademicCalenderBySchool'),
    path('class_teacher_by_academic_calender', ClassTeacherByAcademicCalenderGrade.as_view(),
         name='ClassTeacherByAcademicCalenderGrade'),
    path('grade_list_by_academic_calender/<int:pk>', GradeLisbyAcademicSession.as_view(),
         name='GradeLisbyAcademicSession'),
    path('associate_academic_session/<int:pk>', AssociateAcademicSession.as_view(),
         name='AssociateAcademicSession'),
    path('download_calendar', DownloadCalendar.as_view(),
         name='DownloadCalendar'),
    path('school_calendar_by_school/<int:pk>', SchoolCalendarBySchool.as_view(),
         name='SchoolCalendarBySchool'),

    path('edoofun/section_list_by_school/<int:pk>',
         SectionListBySchool.as_view(), name='Section List By School'),



]
