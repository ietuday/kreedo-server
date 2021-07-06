from django.urls import path
from .views import*
from .edoofun_views import*

urlpatterns = [
     path('child_list_create',
          ChildListCreate.as_view(), name='ChildListCreate'),
     path('child_retrive_update_delete/<int:pk>', ChildRetriveUpdateDestroy.as_view(),
          name='ChildRetriveUpdateDestroy'),
     path('child_detail_by_child/<int:pk>',
          ChildDetailByChild.as_view(), name='ChildDetailByChild'),
     path('child_detail_list_create',
          ChildDetailListCreate.as_view(), name='ChildDetailListCreate'),
     path('child_detail_retrive_update_delete/<int:pk>', ChildDetailRetriveUpdateDestroy.as_view(),
          name='ChildDetailRetriveUpdateDestroy'),
     path('child_session_list_create',
          ChildSessionListCreate.as_view(), name='ChildSessionListCreate'),
     path('child_session_retrive_update_delete/<int:pk>', ChildSessionRetriveUpdateDestroy.as_view(),
          name='ChildSessionRetriveUpdateDestroy'),
     path('child_session_by_child/<int:pk>',
          ChildSessionByChild.as_view(), name='ChildSessionByChild'),
     path('attendance_list_create',
          AttendanceListCreate.as_view(), name='AttendanceListCreate'),
     path('attendance_retrive_update_delete/<int:pk>', AttendanceRetriveUpdateDestroy.as_view(),
          name='AttendanceRetriveUpdateDestroy'),
     path('child_list_according_grade', childListAccordingToClass.as_view(),
          name='childListAccordingToClass'),
     path('attendence_by_academic_session', AttendenceByAcademicSession.as_view(),
          name='Attendence By Academic Session'),
     path('bulk-upload/add-child',
          AddChild.as_view(), name='AddChild'),
     path('bulk-upload/add-child-detail',
          AddChildDetail.as_view(), name='AddChildDetail'),
     path('bulk-upload/add-child-session',
          AddChildSession.as_view(), name='AddChildSession'),

     path('edoofun/register_child', RegisterChild.as_view(),name='Register Parent')

]
