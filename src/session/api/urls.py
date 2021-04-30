from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('school-session_list_create', SchoolSessionListCreate.as_view(),
         name='SchoolSessionListCreate'),
    path('school-session_retrive_update_delete/<int:pk>', SchoolSessionRetriveUpdateDestroy.as_view(),
         name='SchoolSessionRetriveUpdateDestroy'),
    path('academic-session_list_create', AcademicSessionListCreate.as_view(),
         name='AcademicSessionListCreate'),
    path('academic-session_retrive_update_delete/<int:pk>', AcademicSessionRetriveUpdateDestroy.as_view(),
         name='AcademicSessionRetriveUpdateDestroy'),
    path('academic-calender_list_create', AcademicCalenderListCreate.as_view(),
         name='AcademicCalenderListCreate'),
    path('academic-calender_retrive_update_delete/<int:pk>', AcademicCalenderRetriveUpdateDestroy.as_view(),
         name='AcademicCalenderRetriveUpdateDestroy'),


]
