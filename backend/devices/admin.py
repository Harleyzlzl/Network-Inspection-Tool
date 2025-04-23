from django.contrib import admin
from .models import Vendor, DeviceType, Device

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'vendor', 'device_type', 'status', 'last_inspection')
    list_filter = ('status', 'vendor', 'device_type')
    search_fields = ('name', 'ip_address', 'description')
    readonly_fields = ('last_inspection', 'created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'ip_address', 'vendor', 'device_type', 'status')
        }),
        ('连接信息', {
            'fields': ('protocol', 'port', 'username', 'password', 'enable_password')
        }),
        ('其他信息', {
            'fields': ('location', 'description', 'last_inspection', 'created_at', 'updated_at')
        }),
    ) 