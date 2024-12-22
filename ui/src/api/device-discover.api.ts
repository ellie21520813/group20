import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}

export interface DeviceDiscoverTableRow {
  device_id: string;
  name: string;
  hostname: string;
  ip: string;
  updated_date: string;
  status?: string;
  tags?: Tag[];
}

export interface Pagination {
  current?: number;
  pageSize?: number;
  total?: number;
}

export interface DiscoverdDeviceTableData {
  data: DeviceDiscoverTableRow[];
  pagination: Pagination;
}

export const getDiscoverdDeviceTableData = (pagination: Pagination): Promise<DiscoverdDeviceTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post('/v1/device/discover/all', { ...pagination }).then((response) => {
        return response.data;
      }),
    );
  });
};

export const deleteDiscoveredDevice = (device_id: string): Promise<DeviceDiscoverTableRow> => {
  return new Promise((res) => {
    res(
      httpApi.delete(`/v1/device/discover/${device_id}`).then((response) => {
        return response.data;
      }),
    );
  });
};
