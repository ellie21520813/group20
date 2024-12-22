import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}

export interface DeviceTokenTableRow {
  id: number;
  token: string;
  description: string;
  enable: boolean;
  device_id: string;
  owner: string;
  updated_date: string;
  tags?: Tag[];
}

export interface Pagination {
  current?: number;
  pageSize?: number;
  total?: number;
}

export interface FileTableData {
  data: DeviceTokenTableRow[];
  pagination: Pagination;
}

export const getDeviceTokenData = (pagination: Pagination): Promise<FileTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post('/v1/device/token/all', { ...pagination }).then((response) => {
        return response.data;
      }),
    );
  });
};

export const createToken = (description: string) => {
  return httpApi.post('/v1/device/token/add', { description: description });
};

export const deleteToken = (token_id: number) => {
  return httpApi.delete(`/v1/device/token/${token_id}`);
};
