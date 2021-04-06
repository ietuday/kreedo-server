from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.admin import ExportMixin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import*

# Register your models here.
@admin.register(Role)
class RoleAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name','web_kreedo','is_superuser','web_school_account_owner',
                    'web_school_school_admin','mobile_app_accessor','mobile_app_collabrator',
                    'mobile_app_teacher','assigned_to_id']

    search_fields = ['id','name','web_kreedo','is_superuser','web_school_account_owner',
                    'web_school_school_admin','mobile_app_accessor','mobile_app_collabrator',
                    'mobile_app_teacher','assigned_to_id']
    
    list_filter = ['id','name','web_kreedo','is_superuser','web_school_account_owner',
                    'web_school_school_admin','mobile_app_accessor','mobile_app_collabrator',
                    'mobile_app_teacher','assigned_to_id']

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id','username','first_name', 'last_name', 'email')

class UserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UserResource
    list_display = ('id','username','first_name', 'last_name', 'email')
    search_fields = ('id','username','first_name', 'last_name', 'email')
    list_filter = ('id','username','first_name', 'last_name', 'email')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class UserDetailResource(resources.ModelResource):
    class Meta:
        model = UserDetail
        skip_unchanged = True
        report_skipped = True
        exclude = ('id')
        import_id_fields = ['user_obj','phone','relationship_with_child','email_verified',
                    'phone_verified','school']

@admin.register(UserDetail)
class UserDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserDetailResource
    list_display = ['user_obj','phone','relationship_with_child','email_verified',
                    'phone_verified','school']

    search_fields = ['user_obj','phone','relationship_with_child','email_verified',
                    'phone_verified','school']

    list_filter = ['user_obj','phone','relationship_with_child','email_verified',
                    'phone_verified','school']


@admin.register(ReportingTo)
class ReportingToAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','reporting_to','role','user','is_active']
    search_fields = ['id','reporting_to','role','user','is_active']
    list_filter = ['id','reporting_to','role','user','is_active']



