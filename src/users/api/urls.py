from django.urls import path, include
from .views import*


urlpatterns = [
    path('role_list_create', RoleListCreate.as_view(), name='RoleListCreate'),
    path('role_retrive_update_delete/<int:pk>', RoleRetriveUpdateDestroy.as_view(), name='RoleRetriveUpdateDestroy'),
    path('reporting_to_list_create', ReportingToListCreate.as_view(), name='ReportingToListCreate'),
    path('reporting_to_retrive_update_delete/<int:pk>', ReportingToRetriveUpdateDestroy.as_view(), 
        name='ReportingToRetriveUpdateDestroy'),
    path('user_register', UserRegister.as_view(), name='UserRegister'),
]
