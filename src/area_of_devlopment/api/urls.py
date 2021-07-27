from django.urls import path
from .views import*
from .edoofun_views import*

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

     path('bulk-upload/add-concept-skill',
          AddConceptSkill.as_view(), name='AddConceptSkill'),
     path('bulk-upload/add-aod',
          AddAod.as_view(), name='AddConceptSkill'),
         
     path('edoofun/skill_list_by_concept/<int:pk>',
          SkillListByConcept.as_view(), name='Skill List By Concept'),

     path('edoofun/get_concept_list_based_on_subject_id/<int:pk>',
          GetConceptListBasedOnSubjectID.as_view(), name='Get Concept List Based On SubjectID'),
          
]
