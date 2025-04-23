from django.db import models
from django.contrib.auth.models import User
from devices.models import Device


class CommandTemplate(models.Model):
    """巡检命令模板"""
    name = models.CharField(max_length=100, verbose_name='模板名称')
    vendor = models.ForeignKey('devices.Vendor', on_delete=models.CASCADE, related_name='command_templates', verbose_name='适用厂商')
    device_type = models.ForeignKey('devices.DeviceType', on_delete=models.CASCADE, related_name='command_templates', verbose_name='适用设备类型')
    commands = models.TextField(verbose_name='命令列表', help_text='每行一个命令')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '命令模板'
        verbose_name_plural = '命令模板'
        unique_together = ('name', 'vendor', 'device_type')

    def __str__(self):
        return f"{self.name} ({self.vendor.name} - {self.device_type.name})"

    def command_list(self):
        """将命令文本拆分为列表"""
        return [cmd.strip() for cmd in self.commands.split('\n') if cmd.strip()]


class InspectionTask(models.Model):
    """巡检任务"""
    STATUS_CHOICES = [
        ('pending', '待执行'),
        ('running', '执行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('cancelled', '已取消'),
    ]
    
    SCHEDULE_TYPE_CHOICES = [
        ('once', '一次性'),
        ('daily', '每天'),
        ('weekly', '每周'),
        ('monthly', '每月'),
    ]

    name = models.CharField(max_length=100, verbose_name='任务名称')
    devices = models.ManyToManyField(Device, related_name='inspection_tasks', verbose_name='巡检设备')
    command_template = models.ForeignKey(CommandTemplate, on_delete=models.CASCADE, related_name='inspection_tasks', verbose_name='命令模板')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPE_CHOICES, default='once', verbose_name='调度类型')
    scheduled_time = models.DateTimeField(verbose_name='计划执行时间')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='创建者')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    started_at = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')

    class Meta:
        verbose_name = '巡检任务'
        verbose_name_plural = '巡检任务'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class InspectionResult(models.Model):
    """巡检结果"""
    STATUS_CHOICES = [
        ('success', '成功'),
        ('warning', '警告'),
        ('error', '错误'),
    ]

    task = models.ForeignKey(InspectionTask, on_delete=models.CASCADE, related_name='results', verbose_name='巡检任务')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='inspection_results', verbose_name='设备')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success', verbose_name='状态')
    command = models.TextField(verbose_name='执行命令')
    output = models.TextField(verbose_name='命令输出')
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')
    execution_time = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        verbose_name = '巡检结果'
        verbose_name_plural = '巡检结果'
        ordering = ['-execution_time']

    def __str__(self):
        return f"{self.task.name} - {self.device.name} - {self.command[:20]}" 