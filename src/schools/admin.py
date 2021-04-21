from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from schools.models import*

# Register your models here.


@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    search_fields = ['id', 'name', 'is_active']
    list_filter = ['id', 'name', 'is_active']


@admin.register(Section)
class SectionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    search_fields = ['id', 'name', 'is_active']
    list_filter = ['id', 'name', 'is_active']


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'is_kreedo']
    search_fields = ['id', 'name', 'is_active', 'is_kreedo']
    list_filter = ['id', 'name', 'is_active', 'is_kreedo']


@admin.register(License)
class LicenseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'total_no_of_user', 'total_no_of_children', 'licence_from', 'licence_till',
                    'is_active', 'created_by']
    search_fields = ['id', 'total_no_of_user', 'total_no_of_children', 'licence_from', 'licence_till',
                     'is_active', 'created_by']
    list_filter = ['id', 'total_no_of_user', 'total_no_of_children', 'licence_from', 'licence_till',
                   'is_active', 'created_by']


""" School Admin """


@admin.register(School)
class SchoolAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'logo', 'address', 'type',
                    'is_active']
    search_fields = ['id', 'name', 'logo', 'address', 'type',
                     'is_active']
    list_filter = ['id', 'name', 'logo', 'address', 'type',
                   'is_active']


"""Section Subject Teacher Admin"""


@admin.register(SectionSubjectTeacher)
class SectionSubjectTeacherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'subject',
                    'academic_session', 'is_active']
    search_fields = ['id', 'subject',
                     'academic_session', 'is_active']
    list_filter = ['id', 'subject',  'academic_session', 'is_active']


""" Room Admin"""


@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'room_no', 'school', 'is_active']
    search_fields = ['id', 'name', 'room_no', 'school', 'is_active']
    list_filter = ['id', 'name', 'room_no', 'school', 'is_active']
