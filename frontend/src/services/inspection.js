import request from '../utils/request';

export const getTasks = (params) => {
  return request({
    url: '/inspections/tasks/',
    method: 'get',
    params
  });
};

export const getTask = (id) => {
  return request({
    url: `/inspections/tasks/${id}/`,
    method: 'get'
  });
};

export const createTask = (data) => {
  return request({
    url: '/inspections/tasks/',
    method: 'post',
    data
  });
};

export const updateTask = (id, data) => {
  return request({
    url: `/inspections/tasks/${id}/`,
    method: 'put',
    data
  });
};

export const deleteTask = (id) => {
  return request({
    url: `/inspections/tasks/${id}/`,
    method: 'delete'
  });
};

export const executeTask = (id) => {
  return request({
    url: `/inspections/tasks/${id}/execute/`,
    method: 'post'
  });
};

export const cancelTask = (id) => {
  return request({
    url: `/inspections/tasks/${id}/cancel/`,
    method: 'post'
  });
};

export const getResults = (params) => {
  return request({
    url: '/inspections/results/',
    method: 'get',
    params
  });
};

export const getCommandTemplates = (params) => {
  return request({
    url: '/inspections/templates/',
    method: 'get',
    params
  });
};

export const getCommandTemplate = (id) => {
  return request({
    url: `/inspections/templates/${id}/`,
    method: 'get'
  });
};

export const createCommandTemplate = (data) => {
  return request({
    url: '/inspections/templates/',
    method: 'post',
    data
  });
};

export const updateCommandTemplate = (id, data) => {
  return request({
    url: `/inspections/templates/${id}/`,
    method: 'put',
    data
  });
};

export const deleteCommandTemplate = (id) => {
  return request({
    url: `/inspections/templates/${id}/`,
    method: 'delete'
  });
}; 