from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('area-of-devlopment_list_create',
         AreaOfDevlopmentListCreate.as_view(), name='AreaOfDevlopmentListCreate'),

    path('area-of-devlopment_retrive_update_delete/<int:pk>', AreaOfDevlopmentRetriveUpdateDestroy.as_view(),
         name='AreaOfDevlopmentRetriveUpdateDestroy'),

    path('concept_list_create',
         ConceptListCreate.as_view(), name='ConceptListCreate'),

    path('concept_retrive_update_delete/<int:pk>', ConceptRetriveUpdateDestroy.as_view(),
         name='ConceptRetriveUpdateDestroy'),

    path('skill_list_create',
         SkillListCreate.as_view(), name='SkillListCreate'),

    path('skill_retrive_update_delete/<int:pk>', SkillRetriveUpdateDestroy.as_view(),
         name='SkillRetriveUpdateDestroy'),









]
