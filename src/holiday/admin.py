from django.contrib import admin
from holiday.models import*
from import_export.admin import ImportExportModelAdmin

# Register your models here.

""" HolidayType Admin """


@admin.register(HolidayType)
class HolidayTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'holiday_type', 'color_code', 'is_active']
    search_fields = ['id', 'holiday_type', 'color_code', 'is_active']
    list_filter = ['id', 'holiday_type', 'color_code', 'is_active']


@admin.register(SchoolHoliday)
class SchoolHolidayAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'school', 'academic_calender', 'title', 'description', 'holiday_from', 'holiday_till', 'holiday_type', 'is_active'
                    ]
    search_fields = ['id', 'school', 'academic_calender', 'title', 'description', 'holiday_from', 'holiday_till', 'holiday_type', 'is_active'
                     ]
    list_filter = ['id', 'school', 'academic_calender', 'title', 'description', 'holiday_from', 'holiday_till', 'holiday_type', 'is_active'
                   ]


""" School Weakoff Admin """


@admin.register(SchoolWeakOff)
class SchoolWeakOffAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'school', 'academic_calender', 'monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday', 'is_active']
    list_filter = ['id', 'school', 'academic_calender', 'monday', 'tuesday', 'wednesday',
                   'thursday', 'friday', 'saturday', 'sunday', 'is_active']
    search_fields = ['id', 'school', 'academic_calender', 'monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday', 'is_active']
