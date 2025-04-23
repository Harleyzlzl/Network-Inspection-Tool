import request from '../utils/request';

export const getDashboardData = () => {
  return request({
    url: '/core/dashboard/',
    method: 'get'
  });
}; 