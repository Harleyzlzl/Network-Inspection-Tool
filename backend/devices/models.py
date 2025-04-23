from django.db import models


class Vendor(models.Model):
    """设备厂商"""
    name = models.CharField(max_length=100, verbose_name='厂商名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'

    def __str__(self):
        return self.name


class DeviceType(models.Model):
    """设备类型"""
    name = models.CharField(max_length=100, verbose_name='类型名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '设备类型'
        verbose_name_plural = '设备类型'

    def __str__(self):
        return self.name


class Device(models.Model):
    """网络设备"""
    PROTOCOL_CHOICES = [
        ('ssh', 'SSH'),
        ('telnet', 'Telnet'),
        ('snmp', 'SNMP'),
    ]
    
    STATUS_CHOICES = [
        ('online', '在线'),
        ('offline', '离线'),
        ('maintenance', '维护中'),
        ('unknown', '未知'),
    ]

    name = models.CharField(max_length=100, verbose_name='设备名称')
    ip_address = models.CharField(max_length=50, verbose_name='IP地址')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='devices', verbose_name='厂商')
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='devices', verbose_name='设备类型')
    protocol = models.CharField(max_length=10, choices=PROTOCOL_CHOICES, default='ssh', verbose_name='连接协议')
    port = models.IntegerField(default=22, verbose_name='端口')
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    enable_password = models.CharField(max_length=100, blank=True, null=True, verbose_name='启用密码')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown', verbose_name='状态')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='位置')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    last_inspection = models.DateTimeField(blank=True, null=True, verbose_name='上次巡检时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = '设备'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.ip_address})" 