from django.urls import path, re_path
from .views import*
from .edoofun_views import*

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
    path('subject_create', SubjectCreate.as_view(),
         name='SubjectCreate'),

    path('subject_list_by_school', SubjectListBySchool.as_view(),
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
    path('school_update/<int:pk>', SchoolUpdate.as_view(),
         name='SchoolUpdate'),
    path('school_retrive/<int:pk>', SchoolRetrive.as_view(),
         name='SchoolRetrive'),


    path('section-subject-teacher_list_create', SectionSubjectTeacherListCreate.as_view(),
         name='SectionSubjectTeacherListCreate'),
    path('section-subject-teacher_retrive_update_delete/<int:pk>', SectionSubjectTeacherRetriveUpdateDestroy.as_view(),
         name='SectionSubjectTeacherRetriveUpdateDestroy'),
    path('room_list_create', RoomListCreate.as_view(),
         name='RoomListCreate'),
    path('room_retrive_update_delete/<int:pk>', RoomRetriveUpdateDestroy.as_view(),
         name='RoomRetriveUpdateDestroy'),
    path('section_list_by_grade', SectionListByGrade.as_view(),
         name='SectionListByGrade'),
    path('grade_list_by_school', GradeListBySchool.as_view(),
         name='GradeListBySchool'),
    path('subject_room_by_school/<int:pk>', SubjectAndRoomBySchool.as_view(),
         name='SubjectAndRoomBySchool'),
    path('subject_by_academic_session', SubjectByAcademicSession.as_view(),
         name='SubjectByAcademicSession'),
    path('session_grade_section_teacher_by_school/<int:pk>', SessionGradeSectionTeacherSubject.as_view(),
         name='SessionGradeSectionTeacherSubject'),

    path('grade_list_by_kreedo', GradeListByKreedo.as_view(),
         name='GradeListByKreedo'),


    path('bulk-upload/add-subject',
         AddSubject.as_view(), name='AddSubject'),
    path('bulk-upload/add-grade',
         AddGrade.as_view(), name='AddGrade'),

    path('edoofun/get_list_of_active_schools',
         ActiveSchoolList.as_view(), name='Get All School list'),

    path('edoofun/get_list_of_all_schools',
         GetListOfAllSchools.as_view(), name='Get All Active School list'),

    path('edoofun/get_school_detail_based_on_school_id/<int:pk>',
         GetSchoolDetailsBasedOnSchoolID.as_view(), name='Get School  DetailsBasedOn SchoolID'),


    path('edoofun/get_list_of_schools_based_on_account_id',
         GetListOfSchoolsBasedOnAccountID.as_view(), name='Get All Active School list'),

    path('school-assignment', AssignAccountManager.as_view(),
         name='school_assignment'),
    path('teacher_list_according_to_school/<int:pk>',
         TeacherListAccordingToSchool.as_view(), name='teacher_list_based_n_school'),
    path('teacher_subject_association', TeacherSubjectAssociation.as_view(),
         name='teacher_subject_association'),
    path('update_teacher_subject_association', UpdateTeacherSubjectAssociation.as_view(
    ), name='update_teacher_subject_association'),
    path('alter_subject_list', AlterSubjectList.as_view(),
         name='alter_subject_list'),


]
