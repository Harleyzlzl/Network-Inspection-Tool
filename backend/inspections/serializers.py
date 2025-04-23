from rest_framework import serializers
from .models import CommandTemplate, InspectionTask, InspectionResult
from devices.serializers import DeviceSerializer, DeviceListSerializer


class CommandTemplateSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.name')
    device_type_name = serializers.ReadOnlyField(source='device_type.name')
    
    class Meta:
        model = CommandTemplate
        fields = '__all__'


class InspectionResultSerializer(serializers.ModelSerializer):
    device_name = serializers.ReadOnlyField(source='device.name')
    device_ip = serializers.ReadOnlyField(source='device.ip_address')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = InspectionResult
        fields = [
            'id', 'task', 'device', 'device_name', 'device_ip', 'status', 
            'status_display', 'command', 'output', 'error_message', 'execution_time'
        ]


class InspectionTaskSerializer(serializers.ModelSerializer):
    results = InspectionResultSerializer(many=True, read_only=True)
    devices = DeviceListSerializer(many=True, read_only=True)
    device_ids = serializers.PrimaryKeyRelatedField(
        source='devices', 
        queryset=InspectionTask._meta.get_field('devices').related_model.objects.all(),
        many=True, 
        write_only=True
    )
    creator_username = serializers.ReadOnlyField(source='creator.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only=True)
    command_template_name = serializers.ReadOnlyField(source='command_template.name')
    
    class Meta:
        model = InspectionTask
        fields = [
            'id', 'name', 'devices', 'device_ids', 'command_template', 
            'command_template_name', 'status', 'status_display', 'schedule_type', 
            'schedule_type_display', 'scheduled_time', 'creator', 'creator_username',
            'description', 'created_at', 'updated_at', 'started_at', 'finished_at',
            'results'
        ]
        extra_kwargs = {
            'creator': {'read_only': True},
        }
    
    def create(self, validated_data):
        device_ids = validated_data.pop('devices')
        task = InspectionTask.objects.create(**validated_data)
        task.devices.set(device_ids)
        return task
    
    def update(self, instance, validated_data):
        if 'devices' in validated_data:
            device_ids = validated_data.pop('devices')
            instance.devices.set(device_ids)
        return super().update(instance, validated_data)


class InspectionTaskListSerializer(serializers.ModelSerializer):
    device_count = serializers.SerializerMethodField()
    creator_username = serializers.ReadOnlyField(source='creator.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only=True)
    
    class Meta:
        model = InspectionTask
        fields = [
            'id', 'name', 'device_count', 'status', 'status_display', 
            'schedule_type', 'schedule_type_display', 'scheduled_time', 
            'creator_username', 'created_at', 'started_at', 'finished_at'
        ]
    
    def get_device_count(self, obj):
        return obj.devices.count() 