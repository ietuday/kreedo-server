from django.contrib import admin
from .models import*
from import_export.admin import ImportExportModelAdmin

# Register your models here.


""" question answer Admin """

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id','question','answer','is_active']
    search_fields = ['id','question','answer','is_active']
    list_filter = ['id','question','answer','is_active']





