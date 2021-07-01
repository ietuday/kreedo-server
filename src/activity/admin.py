from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from activity.models import*
# Register your models here.

""" Activity Admin"""


@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'objective',
                    'description', 'notes', 'created_by', 'duration', 'is_active']

    search_fields = ['id', 'name', 'type', 'objective',
                     'description', 'notes', 'created_by', 'duration', 'is_active']

    list_filter = ['id', 'name', 'type', 'objective',
                   'description', 'notes', 'created_by', 'duration', 'is_active']


""" Activity Asset Admin """


@admin.register(ActivityAsset)
class ActivityAssetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'activity', 'type', 'activity_data', 'is_active']
    search_fields = ['id', 'activity', 'type', 'activity_data', 'is_active']
    list_filter = ['id', 'activity', 'type', 'activity_data', 'is_active']


""" Group Activity Missed Admin """


@admin.register(ActivityComplete)
class ActivityCompleteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'child','activity','period','is_completed', 'is_active']
    search_fields = ['id','child', 'activity','period','is_completed', 'is_active']
    list_filter = ['id','child', 'activity','period','is_completed', 'is_active']

