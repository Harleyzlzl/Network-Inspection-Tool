import datetime
import logging
from celery import shared_task
from netmiko import ConnectHandler

# 更新异常的导入路径
try:
    # 尝试新版本的导入路径
    from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException
except ImportError:
    # 回退到旧版本的导入路径
    from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

from .models import InspectionTask, InspectionResult
from devices.models import Device

logger = logging.getLogger(__name__)


@shared_task
def run_inspection_task(task_id):
    """
    执行巡检任务
    """
    try:
        task = InspectionTask.objects.get(id=task_id)
        
        # 更新任务状态为执行中
        task.status = 'running'
        task.started_at = datetime.datetime.now()
        task.save()
        
        devices = task.devices.all()
        command_template = task.command_template
        commands = command_template.command_list()
        
        task_success = True
        
        for device in devices:
            # 尝试连接设备
            device_params = {
                'device_type': f"{device.vendor.name.lower()}_{device.device_type.name.lower()}",
                'ip': device.ip_address,
                'username': device.username,
                'password': device.password,
                'port': device.port,
                'secret': device.enable_password,
                'timeout': 30,
            }
            
            try:
                # 建立连接
                with ConnectHandler(**device_params) as conn:
                    # 如果有enable密码，进入特权模式
                    if device.enable_password:
                        conn.enable()
                    
                    # 执行每个命令并记录结果
                    for command in commands:
                        output = conn.send_command(command)
                        
                        # 创建巡检结果
                        InspectionResult.objects.create(
                            task=task,
                            device=device,
                            status='success',
                            command=command,
                            output=output
                        )
                
                # 更新设备的上次巡检时间
                device.last_inspection = datetime.datetime.now()
                device.status = 'online'
                device.save()
                
            except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
                # 连接设备失败
                error_msg = f"连接设备失败: {str(e)}"
                logger.error(f"Device {device.name} ({device.ip_address}) connection failed: {str(e)}")
                
                device.status = 'offline'
                device.save()
                
                # 为每个命令创建失败的结果
                for command in commands:
                    InspectionResult.objects.create(
                        task=task,
                        device=device,
                        status='error',
                        command=command,
                        output='',
                        error_message=error_msg
                    )
                
                task_success = False
                
            except Exception as e:
                # 其他错误
                error_msg = f"巡检执行错误: {str(e)}"
                logger.error(f"Inspection error for device {device.name}: {str(e)}")
                
                # 为每个命令创建失败的结果
                for command in commands:
                    InspectionResult.objects.create(
                        task=task,
                        device=device,
                        status='error',
                        command=command,
                        output='',
                        error_message=error_msg
                    )
                
                task_success = False
        
        # 更新任务状态
        task.finished_at = datetime.datetime.now()
        task.status = 'completed' if task_success else 'failed'
        task.save()
        
        return f"Task {task.name} completed with status: {task.status}"
        
    except InspectionTask.DoesNotExist:
        logger.error(f"Task with ID {task_id} does not exist")
        return f"Task with ID {task_id} does not exist"
    
    except Exception as e:
        logger.error(f"Error running task {task_id}: {str(e)}")
        
        # 如果任务存在，更新状态
        try:
            task = InspectionTask.objects.get(id=task_id)
            task.status = 'failed'
            task.finished_at = datetime.datetime.now()
            task.save()
        except:
            pass
            
        return f"Error running task: {str(e)}" 