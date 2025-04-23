from django.contrib import admin
from .models import CommandTemplate, InspectionTask, InspectionResult

@admin.register(CommandTemplate)
class CommandTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'device_type', 'created_at')
    list_filter = ('vendor', 'device_type')
    search_fields = ('name', 'description')

@admin.register(InspectionTask)
class InspectionTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'creator', 'created_at', 'started_at', 'finished_at')
    list_filter = ('status', 'creator')
    search_fields = ('name', 'description')
    readonly_fields = ('started_at', 'finished_at', 'created_at', 'updated_at')
    filter_horizontal = ('devices',)
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'status', 'description', 'creator')
        }),
        ('巡检范围', {
            'fields': ('devices', 'command_template')
        }),
        ('调度信息', {
            'fields': ('schedule_type', 'scheduled_time', 'started_at', 'finished_at', 'created_at', 'updated_at')
        }),
    )

@admin.register(InspectionResult)
class InspectionResultAdmin(admin.ModelAdmin):
    list_display = ('task', 'device', 'command', 'status', 'execution_time')
    list_filter = ('status', 'device', 'task')
    search_fields = ('command', 'output', 'error_message')
    readonly_fields = ('execution_time',)
    fieldsets = (
        ('巡检信息', {
            'fields': ('task', 'device', 'command', 'status')
        }),
        ('结果详情', {
            'fields': ('output', 'error_message', 'execution_time')
        }),
    ) 