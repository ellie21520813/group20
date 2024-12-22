import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}

export interface DeviceTableRow {
  id: number;
  name: string;
  description: string;
  enable: boolean;
  updated_date: string;
  owner: string;
  tags?: Tag[];
}

export interface DeviceConfigRow {
  id: number;
  device_id: number;
  key: string;
  value: string;
}

export interface Pagination {
  current?: number;
  pageSize?: number;
  total?: number;
}

export interface DeviceTableData {
  data: DeviceTableRow[];
  pagination: Pagination;
}

export interface DeviceConfigTableData {
  data: DeviceConfigRow[];
  pagination: Pagination;
}

export const getDeviceTableData = (pagination: Pagination): Promise<DeviceTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post('/v1/device/all', { ...pagination }).then((response) => {
        return response.data;
      }),
    );
  });
};

export const addDevice = (device: any): Promise<any> => {
  return new Promise((res) => {
    res(
      httpApi.post(`/v1/device/add`, device).then((response) => {
        if (response != undefined) {
          return response.data;
        }
      }),
    );
  });
};

export const deleteDevice = (device_id: string): Promise<DeviceTableRow> => {
  return new Promise((res) => {
    res(
      httpApi.delete(`/v1/device/${device_id}`).then((response) => {
        if (response != undefined) {
          return response.data;
        }
      }),
    );
  });
};

export const getDeviceConfig = (device_id: string, pagination: Pagination): Promise<DeviceConfigTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post(`/v1/device/config/${device_id}/all`, { ...pagination }).then((response) => {
        if (response != undefined) {
          return response.data;
        }
      }),
    );
  });
};

export const getDevice = (device_id: string): Promise<DeviceConfigRow> => {
  return new Promise((res) => {
    res(
      httpApi.get(`/v1/device/${device_id}`).then((response) => {
        if (response != undefined){
          return response.data
        }
      })
    )
  })
}

export const getRtspConfig = (device_id: string): Promise<any> => {
  return new Promise((res) => {
    res(
      httpApi.get(`/v1/device/config/rtsp/${device_id}`).then((response) => {
        if (response != undefined){
          return response.data
        }
      })
    )
  })
}

export const addDeviceConfigs = (deviceConfigs: any): Promise<any> => {
  return new Promise((res) => {
    res(
      httpApi.post(`/v1/device/config/add`, deviceConfigs).then((response) => {
        if (response != undefined) {
          return response.data;
        }
      }),
    );
  });
};

export const deleteDeviceConfig = (id: number): Promise<DeviceConfigRow> => {
  return new Promise((res) => {
    res(
      httpApi.delete(`/v1/device/config/${id}`).then((response) => {
        if (response != undefined) {
          return response.data;
        }
      }),
    );
  });
};
