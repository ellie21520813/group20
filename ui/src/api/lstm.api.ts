import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}

export interface LSTMTableRow {
  id: number;
  name: string;
  description: string;
  ramq_queue: string;
  service: string;
  status: string;
  output: string;
  created_by: string;
  created_date: string;
  updated_date: string;
  tags?: Tag[];
}

export interface Pagination {
  current?: number;
  pageSize?: number;
  total?: number;
}

export interface LSTMTableData {
  data: LSTMTableRow[];
  pagination: Pagination;
}

export interface LSTM {
  name: string;
  description: string;
  file_url: string;
  look_back: number;
  split: number;
  loss_fun: string;
  optimizer: string;
  epochs: number;
  batch_size: number;
}

export const getLSTMTableData = (pagination: Pagination): Promise<LSTMTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post('/v1/task/service/lstm', { ...pagination }).then((response) => {
        return response.data;
      }),
    );
  });
};

export const training = (lstm: LSTM) => {
  return httpApi.post('/v1/lstm/train', lstm);
};
