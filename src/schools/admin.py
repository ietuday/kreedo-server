from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from schools.models import*

# Register your models here.
@admin.register(SchoolType)
class SchoolTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','name','is_active']
    search_fields = ['id','name','is_active']
    list_filter = ['id','name','is_active']

@admin.register(SchoolLicense)
class SchoolLicense(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','total_user','total_children','license_from','license_till',
            'location','created_by','is_active']
    search_fields = ['id','total_user','total_children','license_from','license_till',
            'location','created_by','is_active']
    list_filter = ['id','total_user','total_children','license_from','license_till',
            'location','created_by','is_active']

@admin.register(School)
class SchoolAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','name','school_type','logo','address',
        'license','is_active']
    search_fields = ['id','name','school_type','logo','address',
        'license','is_active']
    list_filter = ['id','name','school_type','logo','address',
        'license','is_active']


