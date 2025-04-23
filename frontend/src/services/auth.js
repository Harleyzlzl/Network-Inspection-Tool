import request from '../utils/request';

export const login = (username, password) => {
  return request({
    url: '/core/login/',
    method: 'post',
    data: { username, password }
  });
};

export const getUserInfo = () => {
  return request({
    url: '/core/users/me/',
    method: 'get'
  });
};

export const updateUserProfile = (data) => {
  return request({
    url: '/core/users/update_me/',
    method: 'put',
    data
  });
};

export const changePassword = (oldPassword, newPassword) => {
  return request({
    url: '/core/users/change_password/',
    method: 'post',
    data: {
      old_password: oldPassword,
      new_password: newPassword
    }
  });
}; 