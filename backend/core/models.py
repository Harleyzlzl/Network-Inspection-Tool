from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='电话')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='部门')
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name='职位')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.user.username


class SystemSetting(models.Model):
    """系统设置"""
    key = models.CharField(max_length=100, unique=True, verbose_name='键名')
    value = models.TextField(verbose_name='值')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='描述')
    is_public = models.BooleanField(default=True, verbose_name='是否公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '系统设置'
        verbose_name_plural = '系统设置'

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


class AuditLog(models.Model):
    """审计日志"""
    ACTION_CHOICES = [
        ('login', '登录'),
        ('logout', '登出'),
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
        ('execute', '执行'),
        ('other', '其他'),
    ]
    
    MODULE_CHOICES = [
        ('devices', '设备管理'),
        ('inspections', '巡检任务'),
        ('reports', '报告管理'),
        ('users', '用户管理'),
        ('system', '系统管理'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs', verbose_name='用户')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='操作')
    module = models.CharField(max_length=20, choices=MODULE_CHOICES, verbose_name='模块')
    object_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='对象ID')
    object_type = models.CharField(max_length=100, blank=True, null=True, verbose_name='对象类型')
    detail = models.TextField(blank=True, null=True, verbose_name='详细信息')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(blank=True, null=True, verbose_name='用户代理')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.get_action_display()} - {self.created_at}" 