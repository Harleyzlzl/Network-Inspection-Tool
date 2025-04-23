import os
import logging
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import tempfile
import json

from .models import Report, ReportTemplate
from inspections.models import InspectionTask, InspectionResult

logger = logging.getLogger(__name__)


@shared_task
def generate_report(report_id):
    """生成巡检报告"""
    try:
        report = Report.objects.get(id=report_id)
        task = report.inspection_task
        
        if report.report_type == 'task':
            return generate_task_report(report, task)
        elif report.report_type == 'device':
            return generate_device_report(report, task)
        elif report.report_type == 'summary':
            return generate_summary_report(report, task)
        else:
            report.status = 'failed'
            report.error_message = f"不支持的报告类型: {report.report_type}"
            report.save()
            return f"Error: {report.error_message}"
    
    except Report.DoesNotExist:
        logger.error(f"Report with ID {report_id} does not exist")
        return f"Error: Report with ID {report_id} does not exist"
    
    except Exception as e:
        logger.error(f"Error generating report {report_id}: {str(e)}")
        
        try:
            report = Report.objects.get(id=report_id)
            report.status = 'failed'
            report.error_message = str(e)
            report.save()
        except:
            pass
            
        return f"Error generating report: {str(e)}"


def generate_task_report(report, task):
    """生成任务报告"""
    try:
        # 获取任务结果数据
        results = InspectionResult.objects.filter(task=task).order_by('device', 'execution_time')
        
        # 按设备分组结果
        device_results = {}
        for result in results:
            device_id = result.device.id
            if device_id not in device_results:
                device_results[device_id] = {
                    'device': result.device,
                    'commands': []
                }
            device_results[device_id]['commands'].append(result)
        
        # 计算统计信息
        total_devices = task.devices.count()
        success_devices = sum(1 for device_id, data in device_results.items() 
                              if all(r.status == 'success' for r in data['commands']))
        warning_devices = sum(1 for device_id, data in device_results.items() 
                              if any(r.status == 'warning' for r in data['commands']) 
                              and not any(r.status == 'error' for r in data['commands']))
        error_devices = sum(1 for device_id, data in device_results.items() 
                            if any(r.status == 'error' for r in data['commands']))
        
        # 生成HTML报告
        context = {
            'report': report,
            'task': task,
            'device_results': device_results.values(),
            'stats': {
                'total_devices': total_devices,
                'success_devices': success_devices,
                'warning_devices': warning_devices,
                'error_devices': error_devices,
            }
        }
        
        html_content = render_to_string('reports/task_report.html', context)
        
        # 根据格式生成报告文件
        if report.format == 'html' or report.format == 'pdf':
            # 所有报告都使用HTML格式
            report_filename = f"{report.name}.html"
            report.file.save(report_filename, ContentFile(html_content))
            
            # 如果是PDF格式，添加一条提示信息
            if report.format == 'pdf':
                report.error_message = "PDF格式暂不支持，已生成HTML格式报告"
                    
        elif report.format == 'excel':
            # 生成JSON格式数据
            report_filename = f"{report.name}.json"
            report_data = {
                'task_name': task.name,
                'devices': [{
                    'name': data['device'].name,
                    'ip': data['device'].ip_address,
                    'commands': [{
                        'command': r.command,
                        'status': r.status,
                        'output': r.output,
                        'error': r.error_message
                    } for r in data['commands']]
                } for data in device_results.values()]
            }
            report.file.save(report_filename, ContentFile(json.dumps(report_data, indent=2)))
        
        # 更新报告状态
        report.status = 'completed'
        report.save()
        
        return f"Report '{report.name}' generated successfully"
        
    except Exception as e:
        report.status = 'failed'
        report.error_message = str(e)
        report.save()
        raise


def generate_device_report(report, task):
    """生成设备报告"""
    # 实际应用中，这里会针对单个设备生成详细报告
    # 为简化示例，这里仅使用任务报告的逻辑
    return generate_task_report(report, task)


def generate_summary_report(report, task):
    """生成汇总报告"""
    # 实际应用中，这里会生成更高层次的汇总报告
    # 为简化示例，这里仅使用任务报告的逻辑
    return generate_task_report(report, task) 