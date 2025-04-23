from rest_framework import serializers
from .models import Vendor, DeviceType, Device


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.name')
    device_type_name = serializers.ReadOnlyField(source='device_type.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    protocol_display = serializers.CharField(source='get_protocol_display', read_only=True)

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'ip_address', 'vendor', 'vendor_name', 'device_type', 
            'device_type_name', 'protocol', 'protocol_display', 'port', 'username', 
            'password', 'enable_password', 'status', 'status_display', 'location', 
            'description', 'last_inspection', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'enable_password': {'write_only': True},
        }


class DeviceListSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.name')
    device_type_name = serializers.ReadOnlyField(source='device_type.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'ip_address', 'vendor_name', 'device_type_name',
            'status', 'status_display', 'last_inspection', 'created_at'
        ] 