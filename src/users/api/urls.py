from django.urls import path, include
from .views import*


urlpatterns = [
    path('role_list_create', RoleListCreate.as_view(), name='RoleListCreate'),
    path('role_retrive_update_delete/<int:pk>', RoleRetriveUpdateDestroy.as_view(), name='RoleRetriveUpdateDestroy'),

]
