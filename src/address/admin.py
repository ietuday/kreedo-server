from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from address.models import*

# Register your models here.

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','country','state','city','address','pincode','is_active']
    search_fields = ['id','country','state','city','address','pincode','is_active'] 
    list_filter = ['id','country','state','city','address','pincode','is_active']

