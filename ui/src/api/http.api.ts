import axios from 'axios';
import { message } from 'antd';
import { AxiosError } from 'axios';
import { ApiError } from '@app/api/ApiError';
import { readToken } from '@app/services/localStorage.service';
import { notificationController } from '@app/controllers/notificationController';

export const httpApi = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

httpApi.interceptors.request.use((config) => {
  config.headers = { ...config.headers, Authorization: `Bearer ${readToken()}` };
  return config;
});

httpApi.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // notificationController.error(error);
    if (error.response?.status === 401) {
      if (!window.location.href.includes('/auth/login')) {
        window.location.href = '/auth/login';
      }
    }
    // notificationController.error({message: String(error)});
    throw error;
  },
);

export interface ApiErrorData {
  detail?: string;
}
