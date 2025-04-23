import request from '../utils/request';

export const getReports = (params) => {
  return request({
    url: '/reports/',
    method: 'get',
    params
  });
};

export const getReport = (id) => {
  return request({
    url: `/reports/${id}/`,
    method: 'get'
  });
};

export const createReport = (data) => {
  return request({
    url: '/reports/',
    method: 'post',
    data
  });
};

export const deleteReport = (id) => {
  return request({
    url: `/reports/${id}/`,
    method: 'delete'
  });
};

export const downloadReport = (id) => {
  window.open(`/api/v1/reports/${id}/download/`, '_blank');
};

export const regenerateReport = (id) => {
  return request({
    url: `/reports/${id}/regenerate/`,
    method: 'post'
  });
};

export const getReportTemplates = (params) => {
  return request({
    url: '/reports/templates/',
    method: 'get',
    params
  });
};

export const getDefaultReportTemplate = (type) => {
  return request({
    url: '/reports/templates/default/',
    method: 'get',
    params: { type }
  });
};

export const createReportTemplate = (data) => {
  return request({
    url: '/reports/templates/',
    method: 'post',
    data
  });
};

export const updateReportTemplate = (id, data) => {
  return request({
    url: `/reports/templates/${id}/`,
    method: 'put',
    data
  });
};

export const deleteReportTemplate = (id) => {
  return request({
    url: `/reports/templates/${id}/`,
    method: 'delete'
  });
}; 