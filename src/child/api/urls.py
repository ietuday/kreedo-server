from django.urls import path
from .views import*


urlpatterns = [
    path('child_list_create',
         ChildListCreate.as_view(), name='ChildListCreate'),

    # path('area-of-devlopment_retrive_update_delete/<int:pk>', AreaOfDevlopmentRetriveUpdateDestroy.as_view(),
    #      name='AreaOfDevlopmentRetriveUpdateDestroy'),
]
