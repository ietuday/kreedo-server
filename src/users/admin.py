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
    list_display = ['id','name','type', 'is_active']

    search_fields = ['id','name','type', 'is_active']
    
    list_filter = ['id','name','type', 'is_active']


# Register your models here.
@admin.register(UserType)
class UserTypeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name', 'is_active']

    search_fields = ['id','name', 'is_active']
    
    list_filter = ['id','name', 'is_active']


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
                    'phone_verified']

@admin.register(UserDetail)
class UserDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserDetailResource
    list_display = ['user_obj','phone','relationship_with_child','email_verified',
                    'phone_verified']

    search_fields = ['user_obj','phone','relationship_with_child','email_verified',
                    'phone_verified']

    list_filter = ['user_obj','phone','relationship_with_child','email_verified',
                    'phone_verified']


@admin.register(ReportingTo)
class ReportingToAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','reporting_to','user_role','user_detail','is_active']
    search_fields = ['id','reporting_to','user_role','user_detail','is_active']
    list_filter = ['id','reporting_to','user_role','user_detail','is_active']


@admin.register(UserRole)
class UserRoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','school','role','user','is_active']
    search_fields = ['id','school','role','user','is_active']
    list_filter = ['id','school','role','user','is_active']



