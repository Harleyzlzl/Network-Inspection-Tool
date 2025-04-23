import React, { useState, useEffect } from 'react';
import { Table, Card, Button, Input, Select, Tag, Space, Popconfirm, message, Typography } from 'antd';
import { PlusOutlined, SearchOutlined, SyncOutlined, DeleteOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import { getDevices, deleteDevice, getVendors, getDeviceTypes } from '../../services/device';

const { Title } = Typography;
const { Option } = Select;

const DeviceList = () => {
  const [loading, setLoading] = useState(false);
  const [devices, setDevices] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [deviceTypes, setDeviceTypes] = useState([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [filters, setFilters] = useState({
    name: '',
    status: '',
    vendor: '',
    device_type: ''
  });
  
  const navigate = useNavigate();

  // 获取设备列表
  const fetchDevices = async (page = 1, size = 10) => {
    try {
      setLoading(true);
      const params = {
        page,
        page_size: size,
        ...filters
      };
      
      // 移除空值
      Object.keys(params).forEach(key => 
        (params[key] === '' || params[key] === undefined) && delete params[key]
      );
      
      const response = await getDevices(params);
      setDevices(response.results || []);
      setTotal(response.count || 0);
      setCurrentPage(page);
      setPageSize(size);
    } catch (error) {
      console.error('Failed to fetch devices:', error);
      message.error('获取设备列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 获取厂商和设备类型
  const fetchOptions = async () => {
    try {
      const [vendorResponse, typeResponse] = await Promise.all([
        getVendors(),
        getDeviceTypes()
      ]);
      setVendors(vendorResponse.results || []);
      setDeviceTypes(typeResponse.results || []);
    } catch (error) {
      console.error('Failed to fetch options:', error);
    }
  };

  useEffect(() => {
    fetchDevices();
    fetchOptions();
  }, []);

  // 处理过滤条件变化
  const handleFilterChange = (key, value) => {
    setFilters({
      ...filters,
      [key]: value
    });
  };

  // 应用过滤条件
  const applyFilters = () => {
    fetchDevices(1, pageSize);
  };

  // 重置过滤条件
  const resetFilters = () => {
    setFilters({
      name: '',
      status: '',
      vendor: '',
      device_type: ''
    });
    fetchDevices(1, pageSize);
  };

  // 处理分页变化
  const handleTableChange = (pagination) => {
    fetchDevices(pagination.current, pagination.pageSize);
  };

  // 处理删除设备
  const handleDelete = async (id) => {
    try {
      await deleteDevice(id);
      message.success('设备删除成功');
      fetchDevices(currentPage, pageSize);
    } catch (error) {
      console.error('Failed to delete device:', error);
      message.error('删除设备失败');
    }
  };

  // 表格列定义
  const columns = [
    {
      title: '设备名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => <Link to={`/devices/${record.id}`}>{text}</Link>
    },
    {
      title: 'IP地址',
      dataIndex: 'ip_address',
      key: 'ip_address'
    },
    {
      title: '厂商',
      dataIndex: 'vendor_name',
      key: 'vendor_name'
    },
    {
      title: '设备类型',
      dataIndex: 'device_type_name',
      key: 'device_type_name'
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status, record) => {
        let color = 'default';
        let text = record.status_display || status;
        
        switch(status) {
          case 'online':
            color = 'success';
            break;
          case 'offline':
            color = 'error';
            break;
          case 'maintenance':
            color = 'warning';
            break;
          default:
            color = 'default';
        }
        
        return <Tag color={color}>{text}</Tag>;
      }
    },
    {
      title: '上次巡检',
      dataIndex: 'last_inspection',
      key: 'last_inspection',
      render: (date) => date ? new Date(date).toLocaleString() : '从未巡检'
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="small">
          <Button 
            type="primary" 
            size="small" 
            icon={<EyeOutlined />}
            onClick={() => navigate(`/devices/${record.id}`)}
          >
            查看
          </Button>
          <Button 
            type="default" 
            size="small" 
            icon={<EditOutlined />}
            onClick={() => navigate(`/devices/${record.id}/edit`)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个设备吗?"
            onConfirm={() => handleDelete(record.id)}
            okText="是"
            cancelText="否"
          >
            <Button 
              type="default" 
              danger 
              size="small" 
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ];

  return (
    <Card>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Title level={2}>设备管理</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/devices/new')}
        >
          添加设备
        </Button>
      </div>
      
      <div style={{ marginBottom: 16 }}>
        <Space wrap>
          <Input
            placeholder="设备名称"
            value={filters.name}
            onChange={(e) => handleFilterChange('name', e.target.value)}
            style={{ width: 200 }}
            allowClear
          />
          
          <Select
            placeholder="设备状态"
            value={filters.status}
            onChange={(value) => handleFilterChange('status', value)}
            style={{ width: 120 }}
            allowClear
          >
            <Option value="online">在线</Option>
            <Option value="offline">离线</Option>
            <Option value="maintenance">维护中</Option>
            <Option value="unknown">未知</Option>
          </Select>
          
          <Select
            placeholder="厂商"
            value={filters.vendor}
            onChange={(value) => handleFilterChange('vendor', value)}
            style={{ width: 150 }}
            allowClear
          >
            {vendors.map(vendor => (
              <Option key={vendor.id} value={vendor.id}>{vendor.name}</Option>
            ))}
          </Select>
          
          <Select
            placeholder="设备类型"
            value={filters.device_type}
            onChange={(value) => handleFilterChange('device_type', value)}
            style={{ width: 150 }}
            allowClear
          >
            {deviceTypes.map(type => (
              <Option key={type.id} value={type.id}>{type.name}</Option>
            ))}
          </Select>
          
          <Button 
            type="primary" 
            icon={<SearchOutlined />} 
            onClick={applyFilters}
          >
            搜索
          </Button>
          
          <Button 
            onClick={resetFilters}
          >
            重置
          </Button>
          
          <Button 
            icon={<SyncOutlined />} 
            onClick={() => fetchDevices(currentPage, pageSize)}
          >
            刷新
          </Button>
        </Space>
      </div>
      
      <Table 
        columns={columns} 
        dataSource={devices} 
        rowKey="id"
        loading={loading}
        pagination={{
          current: currentPage,
          pageSize: pageSize,
          total: total,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total) => `共 ${total} 条记录`
        }}
        onChange={handleTableChange}
      />
    </Card>
  );
};

export default DeviceList; 