from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(SchoolSession)
class SchoolSessionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'school', 'year', 'session_from', 'session_till',
                    'is_current_session', 'is_active']
    search_fields = ['id', 'school', 'year', 'session_from', 'session_till',
                     'is_current_session', 'is_active']
    list_filter = ['id', 'school', 'year', 'session_from', 'session_till',
                   'is_current_session', 'is_active']


@admin.register(AcademicSession)
class AcademicSessionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'session', 'grade', 'section', 'type',
                    'session_from', 'session_till', 'class_teacher', 'is_close', 'is_active', ]
    search_fields = ['id', 'name', 'session', 'grade', 'section', 'type',
                     'session_from', 'session_till', 'class_teacher', 'is_close', 'is_active', ]
    list_filter = ['id', 'name', 'session', 'grade', 'section', 'type',
                   'session_from', 'session_till', 'class_teacher', 'is_close', 'is_active', ]
