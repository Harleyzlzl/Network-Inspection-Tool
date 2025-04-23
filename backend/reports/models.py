from django.db import models
from django.contrib.auth.models import User
from inspections.models import InspectionTask


class Report(models.Model):
    """巡检报告"""
    TYPE_CHOICES = [
        ('task', '任务报告'),
        ('device', '设备报告'),
        ('summary', '汇总报告'),
    ]
    
    FORMAT_CHOICES = [
        ('html', 'HTML'),
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
    ]
    
    STATUS_CHOICES = [
        ('generating', '生成中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]

    name = models.CharField(max_length=200, verbose_name='报告名称')
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='报告类型')
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='html', verbose_name='报告格式')
    inspection_task = models.ForeignKey(InspectionTask, on_delete=models.CASCADE, related_name='reports', verbose_name='关联任务')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generating', verbose_name='状态')
    file = models.FileField(upload_to='reports/%Y/%m/%d/', blank=True, null=True, verbose_name='报告文件')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reports', verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')

    class Meta:
        verbose_name = '巡检报告'
        verbose_name_plural = '巡检报告'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ReportTemplate(models.Model):
    """报告模板"""
    name = models.CharField(max_length=100, verbose_name='模板名称')
    report_type = models.CharField(max_length=20, choices=Report.TYPE_CHOICES, verbose_name='报告类型')
    template_file = models.FileField(upload_to='report_templates/', verbose_name='模板文件')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_templates', verbose_name='创建者')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '报告模板'
        verbose_name_plural = '报告模板'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """如果设置为默认，取消同类型其他默认模板"""
        if self.is_default:
            ReportTemplate.objects.filter(
                report_type=self.report_type, 
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs) 