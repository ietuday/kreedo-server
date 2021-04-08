from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class SchoolSessionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','school','year','session_from','session_till',
                    'is_current_session','is_active']
    search_fields = ['id','school','year','session_from','session_till',
                    'is_current_session','is_active']
    list_filter = ['id','school','year','session_from','session_till',
                    'is_current_session','is_active']


