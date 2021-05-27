from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

""" period Template Admin """


@admin.register(PeriodTemplate)
class PeriodTemplateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'school', 'is_draft', 'is_active']
    search_fields = ['id', 'name', 'school', 'is_draft', 'is_active']
    list_filter = ['id', 'name', 'school',  'is_draft', 'is_active']


""" Period Admin """


@admin.register(Period)
class PeriodAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'room_no','start_date',
                    'description', 'start_time', 'end_time', 'type',  'is_active']
    search_fields = ['id', 'name', 'subject', 'room_no','start_date',
                     'description', 'start_time', 'end_time', 'type', 'is_active']
    list_filter = ['id', 'name', 'subject', 'room_no','start_date',
                   'description', 'start_time', 'end_time', 'type', 'is_active']


""" Period Template Detail Admin"""


@admin.register(PeriodTemplateDetail)
class PeriodTemplateDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'period_template', 'subject', 'room', 'start_time',
                    'end_time', 'type', 'is_active']
    search_fields = ['id', 'period_template', 'subject', 'room', 'start_time',
                     'end_time', 'type', 'is_active']
    list_filter = ['id', 'period_template', 'subject', 'room', 'start_time',
                   'end_time', 'type', 'is_active']


""" Period Template To Grade Admin """


@admin.register(PeriodTemplateToGrade)
class PeriodTemplateToGradeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'academic_session', 'start_date',
                    'end_date', 'period_template', 'is_applied', 'is_active']
    search_fields = ['id', 'academic_session', 'start_date',
                     'end_date', 'period_template', 'is_applied', 'is_active']
    list_filter = ['id', 'academic_session', 'start_date',
                   'end_date', 'period_template', 'is_applied', 'is_active']
