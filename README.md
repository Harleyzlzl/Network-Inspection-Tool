# 网络系统自动化巡检工具

一个基于Python的网络系统自动化巡检工具，采用前后端分离架构设计。

## 功能特点

- 支持多种设备厂商和类型的网络设备巡检
- 设备信息的录入与管理
- 巡检任务的创建与调度
- 巡检结果的展示与分析
- 灵活的配置选项和扩展能力

## 技术栈

### 后端
- Django REST Framework
- Netmiko
- Celery
- PostgreSQL

### 前端
- React
- Ant Design
- Axios
- Echarts

## 快速开始

### 后端设置
```bash
# 克隆仓库
git clone https://github.com/yourusername/network-inspection-tool.git
cd network-inspection-tool/backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动服务
python manage.py runserver
```

### 前端设置
```bash
cd ../frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 项目结构
```
network-inspection-tool/
├── backend/              # Django后端
│   ├── core/             # 核心应用
│   ├── devices/          # 设备管理
│   ├── inspections/      # 巡检任务
│   ├── reports/          # 报告生成
│   └── api/              # API接口
├── frontend/             # React前端
│   ├── src/
│   │   ├── components/   # UI组件
│   │   ├── pages/        # 页面
│   │   ├── services/     # API服务
│   │   └── utils/        # 工具函数
│   └── public/           # 静态资源
└── docs/                 # 文档
``` 