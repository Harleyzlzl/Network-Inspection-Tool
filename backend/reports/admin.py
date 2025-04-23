from django.contrib import admin
from .models import ReportTemplate, Report

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'is_default', 'creator', 'created_at')
    list_filter = ('report_type', 'is_default', 'creator')
    search_fields = ('name', 'description')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'report_type', 'is_default', 'creator')
        }),
        ('模板信息', {
            'fields': ('description', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'format', 'status', 'creator', 'created_at')
    list_filter = ('report_type', 'format', 'status', 'creator')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'file')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'report_type', 'inspection_task', 'format', 'status')
        }),
        ('报告详情', {
            'fields': ('file', 'error_message', 'creator', 'created_at', 'updated_at')
        }),
    ) 