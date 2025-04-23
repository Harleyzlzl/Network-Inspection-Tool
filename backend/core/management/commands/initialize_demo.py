from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from devices.models import Vendor, DeviceType, Device
from inspections.models import CommandTemplate
from core.models import SystemSetting
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '初始化系统演示数据，包括管理员用户、厂商、设备类型等'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            default='admin',
            help='管理员用户名',
        )
        parser.add_argument(
            '--password',
            default='admin',
            help='管理员密码',
        )
        parser.add_argument(
            '--email',
            default='admin@example.com',
            help='管理员邮箱',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('开始初始化系统演示数据...')
        
        # 创建超级用户
        username = options['username']
        password = options['password']
        email = options['email']
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'成功创建超级用户 {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'超级用户 {username} 已存在，跳过创建'))
        
        # 创建设备厂商
        vendors = [
            {'name': '华为', 'description': '华为技术有限公司'},
            {'name': '思科', 'description': 'Cisco Systems, Inc.'},
            {'name': '新华三', 'description': '新华三技术有限公司'},
            {'name': '锐捷', 'description': '锐捷网络股份有限公司'},
        ]
        
        created_vendors = []
        for vendor_data in vendors:
            vendor, created = Vendor.objects.get_or_create(
                name=vendor_data['name'],
                defaults={'description': vendor_data['description']}
            )
            created_vendors.append(vendor)
            if created:
                self.stdout.write(self.style.SUCCESS(f'成功创建厂商: {vendor.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'厂商 {vendor.name} 已存在，跳过创建'))
        
        # 创建设备类型
        device_types = [
            {'name': '路由器', 'description': '网络路由设备'},
            {'name': '交换机', 'description': '网络交换设备'},
            {'name': '防火墙', 'description': '网络安全设备'},
            {'name': '负载均衡器', 'description': '流量负载均衡设备'},
        ]
        
        created_types = []
        for type_data in device_types:
            device_type, created = DeviceType.objects.get_or_create(
                name=type_data['name'],
                defaults={'description': type_data['description']}
            )
            created_types.append(device_type)
            if created:
                self.stdout.write(self.style.SUCCESS(f'成功创建设备类型: {device_type.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'设备类型 {device_type.name} 已存在，跳过创建'))
        
        # 创建示例设备
        if len(created_vendors) > 0 and len(created_types) > 0:
            example_devices = [
                {
                    'name': '核心路由器01',
                    'ip_address': '192.168.1.1',
                    'vendor': created_vendors[0],
                    'device_type': created_types[0],
                    'protocol': 'ssh',
                    'port': 22,
                    'username': 'admin',
                    'password': 'admin123',
                    'status': 'online',
                    'location': '数据中心A区',
                    'description': '核心路由设备，负责网络互联'
                },
                {
                    'name': '核心交换机01',
                    'ip_address': '192.168.1.2',
                    'vendor': created_vendors[1],
                    'device_type': created_types[1],
                    'protocol': 'ssh',
                    'port': 22,
                    'username': 'admin',
                    'password': 'admin123',
                    'status': 'online',
                    'location': '数据中心A区',
                    'description': '核心交换设备，负责内部网络互联'
                },
                {
                    'name': '边界防火墙01',
                    'ip_address': '192.168.1.3',
                    'vendor': created_vendors[2],
                    'device_type': created_types[2],
                    'protocol': 'ssh',
                    'port': 22,
                    'username': 'admin',
                    'password': 'admin123',
                    'status': 'online',
                    'location': '数据中心A区',
                    'description': '边界防火墙，负责网络安全防护'
                },
            ]
            
            for device_data in example_devices:
                device, created = Device.objects.get_or_create(
                    name=device_data['name'],
                    ip_address=device_data['ip_address'],
                    defaults={
                        'vendor': device_data['vendor'],
                        'device_type': device_data['device_type'],
                        'protocol': device_data['protocol'],
                        'port': device_data['port'],
                        'username': device_data['username'],
                        'password': device_data['password'],
                        'status': device_data['status'],
                        'location': device_data['location'],
                        'description': device_data['description']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'成功创建示例设备: {device.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'设备 {device.name} 已存在，跳过创建'))
        
        # 创建命令模板
        if len(created_vendors) > 0 and len(created_types) > 0:
            command_templates = [
                {
                    'name': '华为路由器基本巡检',
                    'vendor': created_vendors[0],
                    'device_type': created_types[0],
                    'commands': 'display version\ndisplay device\ndisplay ip interface brief\ndisplay cpu-usage\ndisplay memory-usage',
                    'description': '华为路由器基本巡检命令集'
                },
                {
                    'name': '思科路由器基本巡检',
                    'vendor': created_vendors[1],
                    'device_type': created_types[0],
                    'commands': 'show version\nshow inventory\nshow ip interface brief\nshow processes cpu\nshow memory statistics',
                    'description': '思科路由器基本巡检命令集'
                },
                {
                    'name': '华为交换机基本巡检',
                    'vendor': created_vendors[0],
                    'device_type': created_types[1],
                    'commands': 'display version\ndisplay device\ndisplay interface brief\ndisplay cpu-usage\ndisplay memory-usage\ndisplay vlan',
                    'description': '华为交换机基本巡检命令集'
                },
            ]
            
            for template_data in command_templates:
                template, created = CommandTemplate.objects.get_or_create(
                    name=template_data['name'],
                    vendor=template_data['vendor'],
                    device_type=template_data['device_type'],
                    defaults={
                        'commands': template_data['commands'],
                        'description': template_data['description']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'成功创建命令模板: {template.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'命令模板 {template.name} 已存在，跳过创建'))
        
        # 创建系统设置
        system_settings = [
            {
                'key': 'system_name',
                'value': '网络自动化巡检系统',
                'description': '系统名称',
                'is_public': True,
            },
            {
                'key': 'system_logo',
                'value': 'logo.png',
                'description': '系统Logo文件名',
                'is_public': True,
            },
            {
                'key': 'dashboard_refresh_interval',
                'value': '60',
                'description': '仪表盘自动刷新间隔（秒），0表示不自动刷新',
                'is_public': True,
            },
        ]
        
        for setting_data in system_settings:
            setting, created = SystemSetting.objects.get_or_create(
                key=setting_data['key'],
                defaults={
                    'value': setting_data['value'],
                    'description': setting_data['description'],
                    'is_public': setting_data['is_public'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'成功创建系统设置: {setting.key}'))
            else:
                self.stdout.write(self.style.WARNING(f'系统设置 {setting.key} 已存在，跳过创建'))
        
        self.stdout.write(self.style.SUCCESS('系统演示数据初始化完成！')) 