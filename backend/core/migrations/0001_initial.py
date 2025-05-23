# Generated by Django 4.2.5 on 2025-04-22 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SystemSetting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.CharField(max_length=100, unique=True, verbose_name="键名"),
                ),
                ("value", models.TextField(verbose_name="值")),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="描述"
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(default=True, verbose_name="是否公开"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
            ],
            options={
                "verbose_name": "系统设置",
                "verbose_name_plural": "系统设置",
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="电话"
                    ),
                ),
                (
                    "department",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="部门"
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="职位"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, null=True, upload_to="avatars/", verbose_name="头像"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "用户信息",
                "verbose_name_plural": "用户信息",
            },
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("login", "登录"),
                            ("logout", "登出"),
                            ("create", "创建"),
                            ("update", "更新"),
                            ("delete", "删除"),
                            ("execute", "执行"),
                            ("other", "其他"),
                        ],
                        max_length=20,
                        verbose_name="操作",
                    ),
                ),
                (
                    "module",
                    models.CharField(
                        choices=[
                            ("devices", "设备管理"),
                            ("inspections", "巡检任务"),
                            ("reports", "报告管理"),
                            ("users", "用户管理"),
                            ("system", "系统管理"),
                        ],
                        max_length=20,
                        verbose_name="模块",
                    ),
                ),
                (
                    "object_id",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="对象ID"
                    ),
                ),
                (
                    "object_type",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="对象类型"
                    ),
                ),
                (
                    "detail",
                    models.TextField(blank=True, null=True, verbose_name="详细信息"),
                ),
                ("ip_address", models.GenericIPAddressField(verbose_name="IP地址")),
                (
                    "user_agent",
                    models.TextField(blank=True, null=True, verbose_name="用户代理"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="时间"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="audit_logs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "审计日志",
                "verbose_name_plural": "审计日志",
                "ordering": ["-created_at"],
            },
        ),
    ]
