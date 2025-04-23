import React, { useState, useEffect } from 'react';
import { Layout, Menu, Dropdown, Button, Avatar } from 'antd';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';
import {
  DashboardOutlined,
  DesktopOutlined,
  SearchOutlined,
  FileTextOutlined,
  UserOutlined,
  SettingOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons';
import { removeToken } from '../utils/auth';

const { Header, Content, Footer, Sider } = Layout;

const MainLayout = ({ userInfo, setIsAuthenticated }) => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedKeys, setSelectedKeys] = useState([]);

  useEffect(() => {
    const pathParts = location.pathname.split('/');
    const mainPath = pathParts[1];
    setSelectedKeys([mainPath || 'dashboard']);
  }, [location]);

  const handleLogout = () => {
    removeToken();
    setIsAuthenticated(false);
    navigate('/login');
  };

  const userMenu = (
    <Menu>
      <Menu.Item key="profile" icon={<UserOutlined />}>
        <Link to="/profile">个人信息</Link>
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
        退出登录
      </Menu.Item>
    </Menu>
  );

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider 
        collapsible 
        collapsed={collapsed} 
        onCollapse={(value) => setCollapsed(value)}
        breakpoint="lg"
      >
        <div className="logo">
          {collapsed ? 'NIS' : '网络巡检系统'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={selectedKeys}
          items={[
            {
              key: 'dashboard',
              icon: <DashboardOutlined />,
              label: <Link to="/dashboard">仪表盘</Link>,
            },
            {
              key: 'devices',
              icon: <DesktopOutlined />,
              label: <Link to="/devices">设备管理</Link>,
            },
            {
              key: 'inspections',
              icon: <SearchOutlined />,
              label: <Link to="/inspections">巡检任务</Link>,
            },
            {
              key: 'reports',
              icon: <FileTextOutlined />,
              label: <Link to="/reports">报告管理</Link>,
            },
            userInfo && userInfo.is_staff ? {
              key: 'users',
              icon: <UserOutlined />,
              label: <Link to="/users">用户管理</Link>,
            } : null,
          ].filter(Boolean)}
        />
      </Sider>
      <Layout className="site-layout">
        <Header className="site-layout-background">
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{ fontSize: '16px', width: 64, height: 64, color: '#fff' }}
          />
          <div className="header-right">
            <Dropdown overlay={userMenu} placement="bottomRight">
              <span className="header-user">
                <Avatar icon={<UserOutlined />} style={{ marginRight: 8 }} />
                {userInfo ? userInfo.username : ''}
              </span>
            </Dropdown>
          </div>
        </Header>
        <Content style={{ margin: '24px 16px 0' }}>
          <div className="site-layout-content">
            <Outlet />
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          网络系统自动化巡检工具 ©{new Date().getFullYear()} 基于Python的Web网络巡检系统
        </Footer>
      </Layout>
    </Layout>
  );
};

export default MainLayout; 