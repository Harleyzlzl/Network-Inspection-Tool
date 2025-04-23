from rest_framework import serializers
from .models import Report, ReportTemplate


class ReportTemplateSerializer(serializers.ModelSerializer):
    creator_username = serializers.ReadOnlyField(source='creator.username')
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    
    class Meta:
        model = ReportTemplate
        fields = [
            'id', 'name', 'report_type', 'report_type_display', 'template_file',
            'is_default', 'creator', 'creator_username', 'description',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'creator': {'read_only': True},
        }


class ReportSerializer(serializers.ModelSerializer):
    creator_username = serializers.ReadOnlyField(source='creator.username')
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    format_display = serializers.CharField(source='get_format_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    task_name = serializers.ReadOnlyField(source='inspection_task.name')
    
    class Meta:
        model = Report
        fields = [
            'id', 'name', 'report_type', 'report_type_display', 'format',
            'format_display', 'inspection_task', 'task_name', 'status',
            'status_display', 'file', 'creator', 'creator_username',
            'created_at', 'updated_at', 'error_message'
        ]
        extra_kwargs = {
            'creator': {'read_only': True},
            'file': {'read_only': True},
            'status': {'read_only': True},
            'error_message': {'read_only': True},
        }


class ReportListSerializer(serializers.ModelSerializer):
    creator_username = serializers.ReadOnlyField(source='creator.username')
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    task_name = serializers.ReadOnlyField(source='inspection_task.name')
    
    class Meta:
        model = Report
        fields = [
            'id', 'name', 'report_type', 'report_type_display', 'task_name',
            'status', 'status_display', 'format', 'creator_username', 'created_at'
        ] 