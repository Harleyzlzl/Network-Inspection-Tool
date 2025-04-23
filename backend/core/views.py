from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
import datetime

from .models import UserProfile, SystemSetting, AuditLog
from .serializers import UserSerializer, SystemSettingSerializer, AuditLogSerializer
from .utils import create_audit_log, get_system_setting


class CustomAuthToken(ObtainAuthToken):
    """自定义令牌认证"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # 创建登录日志
        create_audit_log(request, 'login', 'users', user.id, 'User', f"用户 {user.username} 登录")
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_staff': user.is_staff
        })


class UserViewSet(viewsets.ModelViewSet):
    """用户管理"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_me(self, request):
        """更新当前用户信息"""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # 创建审计日志
        create_audit_log(request, 'update', 'users', user.id, 'User', f"用户 {user.username} 更新个人信息")
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """修改密码"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {"detail": "请提供旧密码和新密码"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return Response(
                {"detail": "旧密码不正确"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        # 创建审计日志
        create_audit_log(request, 'update', 'users', user.id, 'User', f"用户 {user.username} 修改密码")
        
        return Response({"detail": "密码修改成功"})


class SystemSettingViewSet(viewsets.ModelViewSet):
    """系统设置管理"""
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return SystemSetting.objects.all()
        return SystemSetting.objects.filter(is_public=True)
    
    @action(detail=False, methods=['get'])
    def public(self, request):
        """获取公开的系统设置"""
        settings = SystemSetting.objects.filter(is_public=True)
        serializer = self.get_serializer(settings, many=True)
        return Response(serializer.data)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """审计日志查看"""
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = AuditLog.objects.all()
        user_id = self.request.query_params.get('user')
        module = self.request.query_params.get('module')
        action = self.request.query_params.get('action')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if module:
            queryset = queryset.filter(module=module)
        if action:
            queryset = queryset.filter(action=action)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
            
        return queryset


class DashboardView(APIView):
    """仪表盘数据"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 统计设备数据
        from devices.models import Device
        total_devices = Device.objects.count()
        online_devices = Device.objects.filter(status='online').count()
        offline_devices = Device.objects.filter(status='offline').count()
        
        # 统计巡检任务数据
        from inspections.models import InspectionTask
        total_tasks = InspectionTask.objects.count()
        pending_tasks = InspectionTask.objects.filter(status='pending').count()
        running_tasks = InspectionTask.objects.filter(status='running').count()
        completed_tasks = InspectionTask.objects.filter(status='completed').count()
        failed_tasks = InspectionTask.objects.filter(status='failed').count()
        
        # 按设备类型统计
        from devices.models import DeviceType
        device_types = DeviceType.objects.annotate(count=Count('devices')).values('name', 'count')
        
        # 按厂商统计
        from devices.models import Vendor
        vendors = Vendor.objects.annotate(count=Count('devices')).values('name', 'count')
        
        # 最近巡检结果
        from inspections.models import InspectionResult
        recent_results = InspectionResult.objects.order_by('-execution_time')[:10]
        recent_result_data = []
        for result in recent_results:
            recent_result_data.append({
                'id': result.id,
                'task_id': result.task.id,
                'task_name': result.task.name,
                'device_name': result.device.name,
                'device_ip': result.device.ip_address,
                'status': result.status,
                'command': result.command,
                'execution_time': result.execution_time,
            })
        
        # 最近巡检任务
        recent_tasks = InspectionTask.objects.order_by('-created_at')[:5]
        recent_task_data = []
        for task in recent_tasks:
            recent_task_data.append({
                'id': task.id,
                'name': task.name,
                'status': task.status,
                'device_count': task.devices.count(),
                'created_at': task.created_at,
                'creator': task.creator.username,
            })
        
        # 返回仪表盘数据
        data = {
            'devices': {
                'total': total_devices,
                'online': online_devices,
                'offline': offline_devices,
                'by_type': list(device_types),
                'by_vendor': list(vendors),
            },
            'tasks': {
                'total': total_tasks,
                'pending': pending_tasks,
                'running': running_tasks,
                'completed': completed_tasks,
                'failed': failed_tasks,
                'recent': recent_task_data,
            },
            'results': {
                'recent': recent_result_data,
            }
        }
        
        return Response(data) 