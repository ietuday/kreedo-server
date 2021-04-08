from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('school-session_list_create', SchoolSessionListCreate.as_view(), name='SchoolSessionListCreate'),
    path('school-session_retrive_update_delete/<int:pk>', SchoolSessionRetriveUpdateDestroy.as_view(),
         name='SchoolSessionRetriveUpdateDestroy'),

]