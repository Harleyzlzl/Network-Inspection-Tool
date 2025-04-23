import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Spin } from 'antd';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import DeviceList from './pages/device/DeviceList';
import DeviceDetail from './pages/device/DeviceDetail';
import DeviceForm from './pages/device/DeviceForm';
import InspectionTaskList from './pages/inspection/InspectionTaskList';
import InspectionTaskDetail from './pages/inspection/InspectionTaskDetail';
import InspectionTaskForm from './pages/inspection/InspectionTaskForm';
import ReportList from './pages/report/ReportList';
import ReportDetail from './pages/report/ReportDetail';
import ReportForm from './pages/report/ReportForm';
import UserList from './pages/user/UserList';
import UserForm from './pages/user/UserForm';
import UserProfile from './pages/user/UserProfile';
import NotFound from './pages/NotFound';
import MainLayout from './components/MainLayout';
import { getToken, removeToken } from './utils/auth';
import { getUserInfo } from './services/auth';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkAuth = async () => {
      const token = getToken();
      if (token) {
        try {
          const userInfo = await getUserInfo();
          setUserInfo(userInfo);
          setIsAuthenticated(true);
        } catch (error) {
          console.error('Auth check failed:', error);
          removeToken();
          setIsAuthenticated(false);
        }
      } else {
        setIsAuthenticated(false);
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  if (isLoading) {
    return (
      <div className="loading-container">
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={
          isAuthenticated ? (
            <Navigate to="/" replace />
          ) : (
            <Login setIsAuthenticated={setIsAuthenticated} setUserInfo={setUserInfo} />
          )
        }
      />
      <Route
        path="/"
        element={
          isAuthenticated ? (
            <MainLayout userInfo={userInfo} setIsAuthenticated={setIsAuthenticated} />
          ) : (
            <Navigate to="/login" replace state={{ from: location }} />
          )
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        
        <Route path="devices">
          <Route index element={<DeviceList />} />
          <Route path="new" element={<DeviceForm />} />
          <Route path=":id" element={<DeviceDetail />} />
          <Route path=":id/edit" element={<DeviceForm />} />
        </Route>
        
        <Route path="inspections">
          <Route index element={<InspectionTaskList />} />
          <Route path="new" element={<InspectionTaskForm />} />
          <Route path=":id" element={<InspectionTaskDetail />} />
          <Route path=":id/edit" element={<InspectionTaskForm />} />
        </Route>
        
        <Route path="reports">
          <Route index element={<ReportList />} />
          <Route path="new" element={<ReportForm />} />
          <Route path=":id" element={<ReportDetail />} />
        </Route>
        
        <Route path="users">
          <Route index element={<UserList />} />
          <Route path="new" element={<UserForm />} />
          <Route path=":id/edit" element={<UserForm />} />
        </Route>
        
        <Route path="profile" element={<UserProfile />} />
      </Route>
      
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App; 