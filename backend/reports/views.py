from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import os

from .models import Report, ReportTemplate
from .serializers import ReportSerializer, ReportListSerializer, ReportTemplateSerializer
from .tasks import generate_report


class ReportTemplateViewSet(viewsets.ModelViewSet):
    """
    报告模板的CRUD操作
    """
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """获取默认模板"""
        report_type = request.query_params.get('type')
        if not report_type:
            return Response(
                {"detail": "需要指定报告类型参数 'type'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            template = ReportTemplate.objects.get(report_type=report_type, is_default=True)
            serializer = self.get_serializer(template)
            return Response(serializer.data)
        except ReportTemplate.DoesNotExist:
            return Response(
                {"detail": f"未找到报告类型 '{report_type}' 的默认模板"},
                status=status.HTTP_404_NOT_FOUND
            )


class ReportViewSet(viewsets.ModelViewSet):
    """
    报告的CRUD操作
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReportListSerializer
        return ReportSerializer
    
    def perform_create(self, serializer):
        report = serializer.save(creator=self.request.user, status='generating')
        # 启动Celery任务生成报告
        generate_report.delay(report.id)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """下载报告文件"""
        report = self.get_object()
        
        if not report.file:
            return Response(
                {"detail": "报告文件不存在或正在生成中"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 获取文件路径
        file_path = report.file.path
        
        if not os.path.exists(file_path):
            return Response(
                {"detail": "报告文件不存在"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # 根据文件后缀确定内容类型
        filename = os.path.basename(file_path)
        content_type = 'text/html'  # 默认HTML
        
        if filename.endswith('.json'):
            content_type = 'application/json'
        elif filename.endswith('.html'):
            content_type = 'text/html'
        
        # 设置响应
        response = HttpResponse(file_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """重新生成报告"""
        report = self.get_object()
        
        # 更新状态
        report.status = 'generating'
        report.error_message = None
        report.save()
        
        # 启动Celery任务重新生成报告
        generate_report.delay(report.id)
        
        return Response(
            {"detail": f"报告 '{report.name}' 正在重新生成"},
            status=status.HTTP_202_ACCEPTED
        ) 