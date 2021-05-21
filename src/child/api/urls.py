from django.urls import path
from .views import*


urlpatterns = [
    path('child_list_create',
         ChildListCreate.as_view(), name='ChildListCreate'),
    path('child_list', ChildList.as_view(), name='ChildList'),

    path('child-detail_list_create',
         ChildDetailListCreate.as_view(), name='ChildDetailListCreate'),
    path('child-detail_retrive_update_delete/<int:pk>', ChildRetriveUpdateDestroy.as_view(),
         name='ChildRetriveUpdateDestroy'),



    # path('area-of-devlopment_retrive_update_delete/<int:pk>', AreaOfDevlopmentRetriveUpdateDestroy.as_view(),
    #      name='AreaOfDevlopmentRetriveUpdateDestroy'),

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
