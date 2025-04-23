import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { login } from '../services/auth';
import { setToken, setUserInfoToStorage } from '../utils/auth';

const Login = ({ setIsAuthenticated, setUserInfo }) => {
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    try {
      setLoading(true);
      const response = await login(values.username, values.password);
      
      // 保存token和用户信息
      setToken(response.token);
      const userInfo = {
        id: response.user_id,
        username: response.username,
        is_staff: response.is_staff
      };
      setUserInfoToStorage(userInfo);
      
      // 更新应用状态
      setUserInfo(userInfo);
      setIsAuthenticated(true);
      
      message.success('登录成功！');
    } catch (error) {
      console.error('Login failed:', error);
      message.error('登录失败，请检查用户名和密码！');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h1 className="login-form-title">网络巡检系统</h1>
        <Form
          name="login"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          size="large"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名！' }]}
          >
            <Input 
              prefix={<UserOutlined />} 
              placeholder="用户名" 
            />
          </Form.Item>
          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码！' }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码"
            />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              登录
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default Login; 