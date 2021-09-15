from django.contrib import admin
from .models import*
from import_export.admin import ImportExportModelAdmin

# Register your models here.


""" Child Admin """


@admin.register(Child)
class ChildAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'date_of_joining', 'place_of_birth',
                    'blood_group', 'photo', 'registered_by',
                    'reason_for_discontinue', 'is_active']
    search_fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'date_of_joining', 'place_of_birth',
                     'blood_group', 'photo', 'registered_by',
                     'reason_for_discontinue', 'is_active']
    list_filter = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'date_of_joining', 'place_of_birth',
                   'blood_group', 'photo', 'registered_by',
                   'reason_for_discontinue', 'is_active']


""" Child Detail Admin """


@admin.register(ChildDetail)
class ChildDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'child', 'medical_details', 'residence_details', 'emergency_contact_details',
                    'siblings', 'documents', 'is_active']
    search_fields = ['id',  'child', 'medical_details', 'residence_details', 'emergency_contact_details',
                     'siblings', 'documents', 'is_active']
    list_filter = ['id',  'child', 'medical_details', 'residence_details', 'emergency_contact_details',
                   'siblings', 'documents', 'is_active']


""" ChildSession Admin """
@admin.register(ChildSession)
class ChildSessionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','child','session_name','session_type','academic_session',
            'start_date','end_date','is_active']
    search_fields = ['id','child','session_name','session_type','academic_session',
            'start_date','end_date','is_active']
    list_filter = ['id','child','session_name','session_type','academic_session',
            'start_date','end_date','is_active']


""" Attendance Admin """


@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'academic_session', 'marked_status',
                    'attendance_date', 'is_active']
    search_fields = ['id', 'academic_session', 'marked_status',
                     'attendance_date', 'is_active']
    list_filter = ['id', 'academic_session', 'marked_status',
                   'attendance_date', 'is_active']



@admin.register(Block)
class BlockAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        list_display = ['id', 'block_no','is_active','is_done']
