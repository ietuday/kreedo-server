from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from plan.models import*
# Register your models here.


""" Plan Admin"""


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name',  'is_group', 'grade',
                    'range_from', 'range_to', 'previous_kreedo', 'is_active']
    search_fields = ['id', 'name',  'is_group', 'grade',
                     'range_from', 'range_to', 'previous_kreedo', 'is_active']
    list_filter = ['id', 'name',  'is_group', 'grade',
                   'range_from', 'range_to', 'previous_kreedo', 'is_active']


""" Child Plan Admin """


@admin.register(ChildPlan)
class ChildPlanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'child', 'range_of_working_days', 'academic_session', 'current_start_date',
                    'current_end_date', 'published', 'is_active', 'is_close']
    search_fields = ['id', 'name', 'child', 'range_of_working_days', 'academic_session', 'current_start_date',
                     'current_end_date', 'published', 'is_active', 'is_close']
    list_filter = ['id', 'name', 'child', 'range_of_working_days', 'academic_session', 'current_start_date',
                   'current_end_date', 'published', 'is_active', 'is_close']


""" Plan activity Admin"""


@admin.register(PlanActivity)
class PlanActivityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'plan', 'activity', 'sort_no',
                    'is_optional', 'dependent_on', 'is_active']

    search_fields = ['id', 'plan', 'activity', 'sort_no',
                     'is_optional', 'dependent_on', 'is_active']

    list_filter = ['id', 'plan', 'activity', 'sort_no',
                   'is_optional', 'dependent_on', 'is_active']


@admin.register(SubjectSchoolGradePlan)
class SubjectSchoolGradePlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'school',
                    'grade', 'grade_label', 'is_active']
    search_fields = ['id', 'school', 'grade', 'grade_label', 'is_active']
    list_filter = ['id', 'school', 'grade', 'grade_label', 'is_active']
