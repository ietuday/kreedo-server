from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from plan.models import*
# Register your models here.


@admin.register(SubjectSchoolGradePlan)
class SubjectSchoolGradePlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'school', 'subject',
                    'subject_label', 'grade', 'grade_label', 'is_active']
    search_fields = ['id', 'school', 'subject',
                     'subject_label', 'grade', 'grade_label', 'is_active']
    list_filter = ['id', 'school', 'subject',
                   'subject_label', 'grade', 'grade_label', 'is_active']
