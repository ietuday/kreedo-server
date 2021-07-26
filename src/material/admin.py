from django.contrib import admin
from material.models import*
from import_export.admin import ImportExportModelAdmin

# Register your models here.

""" Material admin """


@admin.register(Material)
class MaterialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'photo', 'code', 'is_active']
    search_fields = ['id', 'name', 'description', 'photo', 'code', 'is_active']
    list_filter = ['id', 'name', 'description', 'photo', 'code', 'is_active']


""" Activity Master Supporting  Material Admin """


@admin.register(ActivityMasterSupportingMaterial)
class ActivityMasterSupportingMaterialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'activity', 'is_active']
    search_fields = ['id', 'activity', 'is_active']
    list_filter = ['id', 'activity', 'is_active']
