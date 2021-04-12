from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from package.models import*

# Register your models here.

""" Package Admin """


@admin.register(Package)
class PackageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_active']
    search_fields = ['id', 'name', 'description', 'is_active']
    list_filter = ['id', 'name', 'description', 'is_active']


""" School Package """


@admin.register(SchoolPackage)
class SchoolPackageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'school', 'package',
                    'from_date', 'to_date', 'is_active']
    search_fields = ['id', 'school', 'package',
                     'from_date', 'to_date', 'is_active']
    list_filter = ['id', 'school', 'package',
                   'from_date', 'to_date', 'is_active']
