import request from '../utils/request';

export const getDevices = (params) => {
  return request({
    url: '/devices/',
    method: 'get',
    params
  });
};

export const getDevice = (id) => {
  return request({
    url: `/devices/${id}/`,
    method: 'get'
  });
};

export const createDevice = (data) => {
  return request({
    url: '/devices/',
    method: 'post',
    data
  });
};

export const updateDevice = (id, data) => {
  return request({
    url: `/devices/${id}/`,
    method: 'put',
    data
  });
};

export const deleteDevice = (id) => {
  return request({
    url: `/devices/${id}/`,
    method: 'delete'
  });
};

export const checkDeviceConnectivity = (id) => {
  return request({
    url: `/devices/${id}/check_connectivity/`,
    method: 'post'
  });
};

export const getVendors = () => {
  return request({
    url: '/devices/vendors/',
    method: 'get'
  });
};

export const getDeviceTypes = () => {
  return request({
    url: '/devices/types/',
    method: 'get'
  });
}; 