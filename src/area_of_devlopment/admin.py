from django.contrib import admin
from .models import*
from import_export.admin import ImportExportModelAdmin
# Register your models here.

""" Area Of Devlopment Admin """


@admin.register(AreaOfDevlopment)
class AreaOfDevlopmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_active']
    search_fields = ['id', 'name', 'description', 'is_active']
    list_filter = ['id', 'name', 'description', 'is_active']


""" Concept Admin """


@admin.register(Concept)
class ConceptAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'aod', 'is_active']
    search_fields = ['id', 'name', 'description', 'aod', 'is_active']
    list_filter = ['id', 'name', 'description', 'aod', 'is_active']


""" Skill Admin """


@admin.register(Skill)
class SkillAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'concept', 'is_active',
                    'threshold_percentage']
    search_fields = ['id', 'name', 'description', 'concept', 'is_active',
                     'threshold_percentage']
    list_filter = ['id', 'name', 'description', 'concept', 'is_active',
                   'threshold_percentage']
