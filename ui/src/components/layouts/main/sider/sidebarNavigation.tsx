import React from 'react';
import {
  CompassOutlined,
  DashboardOutlined,
  FormOutlined,
  HomeOutlined,
  LayoutOutlined,
  LineChartOutlined,
  TableOutlined,
  UserOutlined,
  BlockOutlined,
  FileOutlined,
  TeamOutlined,
  ClusterOutlined,
} from '@ant-design/icons';

export interface SidebarNavigationItem {
  title: string;
  key: string;
  url?: string;
  display?: boolean;
  children?: SidebarNavigationItem[];
  icon?: React.ReactNode;
}

export const sidebarNavigation: SidebarNavigationItem[] = [
  {
    title: 'common.userPage',
    key: 'users',
    icon: <TeamOutlined />,
    url: '/users',
  },
  {
    title: 'common.filesPage',
    key: 'files',
    icon: <FileOutlined />,
    url: '/files',
  },
  {
    title: 'Device',
    key: 'devices',
    icon: <ClusterOutlined />,
    children: [
      {
        title: 'Devices',
        key: 'list-devices',
        url: '/device/list',
      },
      {
        title: 'Tokens',
        key: 'device-token',
        url: '/device/token',
      },
    ],
  },
  {
    title: 'common.apps',
    key: 'apps',
    icon: <HomeOutlined />,
    children: [
      {
        title: 'LSTM',
        key: 'lstm',
        url: '/apps/lstm',
      },
      {
        title: 'Redis Message',
        key: 'redis-message',
        url: '/apps/redis-message',
      },
      {
        title: 'MQTT',
        key: 'mqtt',
        url: '/apps/mqtt',
      },
    ],
  },
  {
    title: 'common.authPages',
    key: 'auth',
    icon: <UserOutlined />,
    display: false,
    children: [
      {
        title: 'common.login',
        key: 'login',
        url: '/auth/login',
      },
      {
        title: 'common.signUp',
        key: 'singUp',
        url: '/auth/sign-up',
      },
      {
        title: 'common.lock',
        key: 'lock',
        url: '/auth/lock',
      },
      {
        title: 'common.forgotPass',
        key: 'forgotPass',
        url: '/auth/forgot-password',
      },
      {
        title: 'common.securityCode',
        key: 'securityCode',
        url: '/auth/security-code',
      },
      {
        title: 'common.newPassword',
        key: 'newPass',
        url: '/auth/new-password',
      },
    ],
  },
  {
    title: 'common.pages',
    key: 'pages',
    icon: <LayoutOutlined />,
    display: false,
    children: [
      {
        title: 'common.profilePage',
        key: 'profile',
        url: '/profile',
      },
      {
        title: 'common.serverError',
        key: 'serverError',
        url: '/server-error',
      },
      {
        title: 'common.clientError',
        key: '404Error',
        url: '/404',
      },
    ],
  },
];
