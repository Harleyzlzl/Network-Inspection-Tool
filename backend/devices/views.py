from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Vendor, DeviceType, Device
from .serializers import (
    VendorSerializer, DeviceTypeSerializer, 
    DeviceSerializer, DeviceListSerializer
)


class VendorViewSet(viewsets.ModelViewSet):
    """
    设备厂商的CRUD操作
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]


class DeviceTypeViewSet(viewsets.ModelViewSet):
    """
    设备类型的CRUD操作
    """
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    网络设备的CRUD操作
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DeviceListSerializer
        return DeviceSerializer
    
    def get_queryset(self):
        queryset = Device.objects.all()
        vendor = self.request.query_params.get('vendor')
        device_type = self.request.query_params.get('device_type')
        status = self.request.query_params.get('status')
        
        if vendor:
            queryset = queryset.filter(vendor_id=vendor)
        if device_type:
            queryset = queryset.filter(device_type_id=device_type)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def check_connectivity(self, request, pk=None):
        """
        测试与设备的连接性
        """
        device = self.get_object()
        # 这里应该添加实际的连接测试逻辑，使用netmiko
        # 这只是一个模拟示例
        try:
            # 实际应用中这里会使用netmiko尝试连接设备
            connected = True
            message = "连接成功"
            device.status = 'online'
            device.save()
        except Exception as e:
            connected = False
            message = f"连接失败: {str(e)}"
            device.status = 'offline'
            device.save()
            
        return Response({
            'connected': connected,
            'message': message,
            'device_id': device.id,
            'device_name': device.name,
            'status': device.status
        }) 