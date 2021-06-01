from django.urls import path
from .views import*


urlpatterns = [
     path('child_list_create',
         ChildListCreate.as_view(), name='ChildListCreate'),
     path('child_retrive_update_delete/<int:pk>', ChildRetriveUpdateDestroy.as_view(),
         name='ChildRetriveUpdateDestroy'),
     path('child_detail_by_child/<int:pk>',
         ChildDetailByChild.as_view(), name='ChildDetailByChild'),
     path('child-detail_list_create',
         ChildDetailListCreate.as_view(), name='ChildDetailListCreate'),
     path('child-detail_retrive_update_delete/<int:pk>', ChildDetailRetriveUpdateDestroy.as_view(),
         name='ChildDetailRetriveUpdateDestroy'),
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



]
