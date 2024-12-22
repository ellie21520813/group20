import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// no lazy loading for auth pages to avoid flickering
const AuthLayout = React.lazy(() => import('@app/components/layouts/AuthLayout/AuthLayout'));

import LoginPage from '@app/pages/LoginPage';
import SignUpPage from '@app/pages/SignUpPage';
import ForgotPasswordPage from '@app/pages/ForgotPasswordPage';
import SecurityCodePage from '@app/pages/SecurityCodePage';
import NewPasswordPage from '@app/pages/NewPasswordPage';
import LockPage from '@app/pages/LockPage';

import MainLayout from '@app/components/layouts/main/MainLayout/MainLayout';
import ProfileLayout from '@app/components/profile/ProfileLayout';
import RequireAuth from '@app/components/router/RequireAuth';
import { withLoading } from '@app/hocs/withLoading.hoc';

const ServerErrorPage = React.lazy(() => import('@app/pages/ServerErrorPage'));
const Error404Page = React.lazy(() => import('@app/pages/Error404Page'));
const PersonalInfoPage = React.lazy(() => import('@app/pages/PersonalInfoPage'));
const SecuritySettingsPage = React.lazy(() => import('@app/pages/SecuritySettingsPage'));
const NotificationsPage = React.lazy(() => import('@app/pages/NotificationsPage'));
const PaymentsPage = React.lazy(() => import('@app/pages/PaymentsPage'));
const UsersTablePage = React.lazy(() => import('@app/pages/UsersPage'));
const FilesTablePage = React.lazy(() => import('@app/pages/FilesPage'));
const LSTMTablePage = React.lazy(() => import('@app/pages/LSTMPage'));
const DeviceTokenPage = React.lazy(() => import('@app/pages/DeviceTokenPage'));

const RedisMessagePage = React.lazy(() => import('@app/pages/RedisMessagePage'));
const MQTTPage = React.lazy(() => import('@app/pages/MQTTPage'));
const DevicePage = React.lazy(() => import('@app/pages/DevicePage'));
const DeviceDetailsPage = React.lazy(() => import('@app/pages/DeviceDetailsPage'));
const DeviceServicesPage = React.lazy(() => import('@app/pages/DeviceServicesPage'));
const Logout = React.lazy(() => import('./Logout'));

const UsersTable = withLoading(UsersTablePage);
const FilesTable = withLoading(FilesTablePage);
const LSTMTable = withLoading(LSTMTablePage);
const RedisMessage = withLoading(RedisMessagePage);
const MQTT = withLoading(MQTTPage);
const Device = withLoading(DevicePage);
const DeviceToken = withLoading(DeviceTokenPage);
const DeviceDetails = withLoading(DeviceDetailsPage);
const DeviceServices = withLoading(DeviceServicesPage);

const ServerError = withLoading(ServerErrorPage);
const Error404 = withLoading(Error404Page);

// Profile
const PersonalInfo = withLoading(PersonalInfoPage);
const SecuritySettings = withLoading(SecuritySettingsPage);
const Notifications = withLoading(NotificationsPage);
const Payments = withLoading(PaymentsPage);

const AuthLayoutFallback = withLoading(AuthLayout);
const LogoutFallback = withLoading(Logout);

export const AppRouter: React.FC = () => {
  const protectedLayout = (
    <RequireAuth>
      <MainLayout />
    </RequireAuth>
  );

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={protectedLayout}>
          <Route index element={<PersonalInfo />} />
          <Route path="apps">
            <Route path="lstm" element={<LSTMTable />} />
            <Route path="redis-message" element={<RedisMessage />} />
            <Route path="mqtt" element={<MQTT />} />
          </Route>
          <Route path="users" element={<UsersTable />}></Route>
          <Route path="files" element={<FilesTable />}></Route>
          <Route path="device">
            <Route path="list" element={<Device />}></Route>
            <Route path="token" element={<DeviceToken />}></Route>
            <Route path="details" element={<DeviceDetails />}></Route>
            <Route path="services" element={<DeviceServices />}></Route>
          </Route>
          <Route path="server-error" element={<ServerError />} />
          <Route path="404" element={<Error404 />} />
          <Route path="profile" element={<ProfileLayout />}>
            <Route path="personal-info" element={<PersonalInfo />} />
            <Route path="security-settings" element={<SecuritySettings />} />
            <Route path="notifications" element={<Notifications />} />
            <Route path="payments" element={<Payments />} />
          </Route>
        </Route>
        <Route path="/auth" element={<AuthLayoutFallback />}>
          <Route path="login" element={<LoginPage />} />
          <Route path="sign-up" element={<SignUpPage />} />
          <Route
            path="lock"
            element={
              <RequireAuth>
                <LockPage />
              </RequireAuth>
            }
          />
          <Route path="forgot-password" element={<ForgotPasswordPage />} />
          <Route path="security-code" element={<SecurityCodePage />} />
          <Route path="new-password" element={<NewPasswordPage />} />
        </Route>
        <Route path="/logout" element={<LogoutFallback />} />
      </Routes>
    </BrowserRouter>
  );
};
