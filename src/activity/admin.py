from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from activity.models import*
# Register your models here.

""" Activity Admin"""


@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ['id', 'name', 'type', 'objective',
                   'description', 'notes', 'created_by', 'duration', 'is_active']

    search_fields = ['id', 'name', 'type', 'objective',
                     'description', 'notes', 'created_by', 'duration', 'is_active']

    list_filter = ['id', 'name', 'type', 'objective',
                   'description', 'notes', 'created_by', 'duration', 'is_active']
