import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}


export interface CameraConfig {
  ip: string;
  port: number;
  protocol: string;
  username: string;
  password: string;
  path: string;
  owner: string;
}


export const getRtspConfig = (device_id: string): Promise<string> => {
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