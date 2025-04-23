import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Typography, Spin } from 'antd';
import { 
  DesktopOutlined, 
  CheckCircleOutlined, 
  CloseCircleOutlined, 
  ClockCircleOutlined, 
  WarningOutlined 
} from '@ant-design/icons';
import ReactEcharts from 'echarts-for-react';
import { getDashboardData } from '../services/dashboard';
import { Link } from 'react-router-dom';

const { Title } = Typography;

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await getDashboardData();
        setDashboardData(data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const deviceStatusOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      data: ['在线', '离线', '其他']
    },
    series: [
      {
        name: '设备状态',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: dashboardData ? [
          { value: dashboardData.devices.online, name: '在线' },
          { value: dashboardData.devices.offline, name: '离线' },
          { value: dashboardData.devices.total - dashboardData.devices.online - dashboardData.devices.offline, name: '其他' }
        ] : []
      }
    ]
  };

  const taskStatusOption = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: '任务状态',
        type: 'pie',
        radius: '50%',
        data: dashboardData ? [
          { value: dashboardData.tasks.completed, name: '已完成' },
          { value: dashboardData.tasks.running, name: '执行中' },
          { value: dashboardData.tasks.pending, name: '待执行' },
          { value: dashboardData.tasks.failed, name: '失败' }
        ] : [],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  const deviceTypeOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: dashboardData?.devices.by_type.map(item => item.name) || []
    },
    series: [
      {
        name: '数量',
        type: 'bar',
        data: dashboardData?.devices.by_type.map(item => item.count) || []
      }
    ]
  };

  const recentTaskColumns = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => <Link to={`/inspections/${record.id}`}>{text}</Link>
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        let color = 'default';
        let icon = null;
        
        switch(status) {
          case 'completed':
            color = 'success';
            icon = <CheckCircleOutlined />;
            break;
          case 'running':
            color = 'processing';
            icon = <ClockCircleOutlined />;
            break;
          case 'pending':
            color = 'warning';
            icon = <ClockCircleOutlined />;
            break;
          case 'failed':
            color = 'error';
            icon = <CloseCircleOutlined />;
            break;
          default:
            icon = <WarningOutlined />;
        }
        
        return (
          <Tag icon={icon} color={color}>
            {status === 'completed' ? '已完成' : 
             status === 'running' ? '执行中' : 
             status === 'pending' ? '待执行' : 
             status === 'failed' ? '失败' : status}
          </Tag>
        );
      }
    },
    {
      title: '设备数',
      dataIndex: 'device_count',
      key: 'device_count'
    },
    {
      title: '创建者',
      dataIndex: 'creator',
      key: 'creator'
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at'
    }
  ];

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  return (
    <div className="dashboard">
      <Title level={2}>系统仪表盘</Title>
      
      <Row gutter={16}>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="设备总数"
              value={dashboardData?.devices.total || 0}
              prefix={<DesktopOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="在线设备"
              value={dashboardData?.devices.online || 0}
              valueStyle={{ color: '#3f8600' }}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="离线设备"
              value={dashboardData?.devices.offline || 0}
              valueStyle={{ color: '#cf1322' }}
              prefix={<CloseCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="dashboard-card">
            <Statistic
              title="巡检任务"
              value={dashboardData?.tasks.total || 0}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>
      
      <Row gutter={16}>
        <Col span={8}>
          <Card title="设备状态" className="dashboard-card">
            <ReactEcharts option={deviceStatusOption} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="任务状态" className="dashboard-card">
            <ReactEcharts option={taskStatusOption} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="设备类型分布" className="dashboard-card">
            <ReactEcharts option={deviceTypeOption} style={{ height: 300 }} />
          </Card>
        </Col>
      </Row>
      
      <Row gutter={16}>
        <Col span={24}>
          <Card title="最近巡检任务" className="dashboard-card">
            <Table 
              dataSource={dashboardData?.tasks.recent || []} 
              columns={recentTaskColumns} 
              rowKey="id"
              pagination={false}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 