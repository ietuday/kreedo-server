from django.contrib import admin
from .models import*
from import_export.admin import ImportExportModelAdmin

# Register your models here.


""" Child Admin """


@admin.register(Child)
class ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'date_of_joining', 'place_of_birth',
                    'blood_group', 'photo', 'registered_by',
                    'academic_session', 'reason_for_discontinue', 'is_active']
    search_fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'date_of_joining', 'place_of_birth',
                     'blood_group', 'photo', 'registered_by',
                     'academic_session', 'reason_for_discontinue', 'is_active']
    list_filter = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'date_of_joining', 'place_of_birth',
                   'blood_group', 'photo', 'registered_by',
                   'academic_session', 'reason_for_discontinue', 'is_active']


""" Child Detail Admin """


@admin.register(ChildDetail)
class ChildDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'child', 'medical_details', 'recidence_details', 'emergency_of_contact_details',
                    'siblings_details', 'document_checklist', 'is_active']
    search_fields = ['id',  'child', 'medical_details', 'recidence_details', 'emergency_of_contact_details',
                     'siblings_details', 'document_checklist', 'is_active']
    list_filter = ['id',  'child', 'medical_details', 'recidence_details', 'emergency_of_contact_details',
                   'siblings_details', 'document_checklist', 'is_active']


""" Attendance Admin """


@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'academic_session', 'marked_status',
                    'attendance_date', 'is_active']
    search_fields = ['id', 'academic_session', 'marked_status',
                     'attendance_date', 'is_active']
    list_filter = ['id', 'academic_session', 'marked_status',
                   'attendance_date', 'is_active']
