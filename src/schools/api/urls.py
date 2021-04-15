from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('grade_list_create', GradeListCreate.as_view(), name='GradeListCreate'),
    path('grade_retrive_update_delete/<int:pk>', GradeRetriveUpdateDestroy.as_view(),
         name='GradeRetriveUpdateDestroy'),
    path('section_list_create', SectionListCreate.as_view(),
         name='SectionListCreate'),
    path('section_retrive_update_delete/<int:pk>', SectionRetriveUpdateDestroy.as_view(),
         name='SectionRetriveUpdateDestroy'),
    path('subject_list_create', SubjectListCreate.as_view(),
         name='SubjectListCreate'),
    path('subject_retrive_update_delete/<int:pk>', SubjectRetriveUpdateDestroy.as_view(),
         name='SubjectRetriveUpdateDestroy'),
    path('license_list_create', LicenseListCreate.as_view(),
         name='LicenseListCreate'),
    path('license_retrive_update_delete/<int:pk>', LicenseRetriveUpdateDestroy.as_view(),
         name='LicenseRetriveUpdateDestroy'),
    path('school_list_create', SchoolListCreate.as_view(), name='SchoolListCreate'),
    path('school_retrive_update_delete/<int:pk>', SchoolRetriveUpdateDestroy.as_view(),
         name='SchoolRetriveUpdateDestroy'),
    path('section-subject-teacher_list_create', SectionSubjectTeacherListCreate.as_view(),
         name='SectionSubjectTeacherListCreate'),

    path('section-subject-teacher_retrive_update_delete/<int:pk>', SectionSubjectTeacherRetriveUpdateDestroy.as_view(),
         name='SectionSubjectTeacherRetriveUpdateDestroy'),




]
