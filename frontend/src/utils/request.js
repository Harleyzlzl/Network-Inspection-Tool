import axios from 'axios';
import { getToken, removeToken } from './auth';
import { message } from 'antd';

// 创建axios实例
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('Response error:', error);
    
    if (error.response) {
      const { status, data } = error.response;
      
      // 处理401认证错误
      if (status === 401) {
        removeToken();
        message.error('登录已过期，请重新登录');
        window.location.href = '/login';
      }
      
      // 显示后端返回的错误信息
      if (data && data.detail) {
        message.error(data.detail);
      } else if (data && typeof data === 'object') {
        // 处理表单错误
        const errMsgs = [];
        Object.keys(data).forEach(key => {
          if (Array.isArray(data[key])) {
            errMsgs.push(`${key}: ${data[key].join(', ')}`);
          } else {
            errMsgs.push(`${key}: ${data[key]}`);
          }
        });
        
        if (errMsgs.length > 0) {
          message.error(errMsgs.join('\n'));
        }
      } else {
        // 默认错误消息
        switch (status) {
          case 400:
            message.error('请求参数错误');
            break;
          case 403:
            message.error('没有权限进行此操作');
            break;
          case 404:
            message.error('请求的资源不存在');
            break;
          case 500:
            message.error('服务器内部错误');
            break;
          default:
            message.error(`请求失败: ${status}`);
        }
      }
    } else {
      // 网络连接问题
      message.error('网络连接失败，请检查网络设置');
    }
    
    return Promise.reject(error);
  }
);

export default request; 