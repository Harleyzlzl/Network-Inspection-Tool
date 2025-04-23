import json
from .models import AuditLog

def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def create_audit_log(request, action, module, object_id=None, object_type=None, detail=None):
    """创建审计日志"""
    try:
        # 如果detail是字典或列表，转为JSON字符串
        if isinstance(detail, (dict, list)):
            detail = json.dumps(detail)
            
        user = request.user if request.user.is_authenticated else None
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        AuditLog.objects.create(
            user=user,
            action=action,
            module=module,
            object_id=object_id,
            object_type=object_type,
            detail=detail,
            ip_address=ip_address,
            user_agent=user_agent
        )
    except Exception as e:
        # 日志记录不应影响正常流程
        print(f"Error creating audit log: {str(e)}")
        
        
def get_system_setting(key, default=None):
    """获取系统设置"""
    from .models import SystemSetting
    try:
        setting = SystemSetting.objects.get(key=key)
        return setting.value
    except SystemSetting.DoesNotExist:
        return default 