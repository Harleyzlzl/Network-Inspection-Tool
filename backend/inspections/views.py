from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import CommandTemplate, InspectionTask, InspectionResult
from .serializers import (
    CommandTemplateSerializer, InspectionTaskSerializer, 
    InspectionTaskListSerializer, InspectionResultSerializer
)
from .tasks import run_inspection_task


class CommandTemplateViewSet(viewsets.ModelViewSet):
    """
    命令模板的CRUD操作
    """
    queryset = CommandTemplate.objects.all()
    serializer_class = CommandTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = CommandTemplate.objects.all()
        vendor = self.request.query_params.get('vendor')
        device_type = self.request.query_params.get('device_type')
        
        if vendor:
            queryset = queryset.filter(vendor_id=vendor)
        if device_type:
            queryset = queryset.filter(device_type_id=device_type)
            
        return queryset


class InspectionTaskViewSet(viewsets.ModelViewSet):
    """
    巡检任务的CRUD操作
    """
    queryset = InspectionTask.objects.all()
    serializer_class = InspectionTaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InspectionTaskListSerializer
        return InspectionTaskSerializer
    
    def get_queryset(self):
        queryset = InspectionTask.objects.all()
        status = self.request.query_params.get('status')
        
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """
        执行巡检任务
        """
        task = self.get_object()
        
        # 检查任务是否可以执行
        if task.status in ['running', 'pending']:
            return Response(
                {"detail": "任务已在执行队列中或正在执行"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新任务状态
        task.status = 'pending'
        task.save()
        
        # 启动Celery任务执行巡检
        run_inspection_task.delay(task.id)
        
        return Response(
            {"detail": f"任务 '{task.name}' 已提交执行"},
            status=status.HTTP_202_ACCEPTED
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        取消巡检任务
        """
        task = self.get_object()
        
        if task.status not in ['pending', 'running']:
            return Response(
                {"detail": "只能取消待执行或执行中的任务"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = 'cancelled'
        task.finished_at = timezone.now()
        task.save()
        
        # 实际上，取消正在执行的任务需要更复杂的Celery任务管理
        # 这里简化处理，只更新状态
        
        return Response(
            {"detail": f"任务 '{task.name}' 已取消"},
            status=status.HTTP_200_OK
        )


class InspectionResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    巡检结果的只读操作
    """
    queryset = InspectionResult.objects.all()
    serializer_class = InspectionResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = InspectionResult.objects.all()
        task_id = self.request.query_params.get('task')
        device_id = self.request.query_params.get('device')
        status = self.request.query_params.get('status')
        
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset 