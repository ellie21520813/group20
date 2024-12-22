import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}

export interface TaskTableRow {
  id: number;
  name: string;
  description: string;
  ramq_queue: string;
  service: string;
  status: string;
  output: string;
  created_by: string;
  created_date: Date;
  updated_date: Date;
  tags?: Tag[];
}

export interface Pagination {
  current?: number;
  pageSize?: number;
  total?: number;
}

export interface TaskTableData {
  data: TaskTableRow[];
  pagination: Pagination;
}

export const getTask = (pagination: Pagination): Promise<TaskTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post('/v1/task', { ...pagination }).then((response) => {
        return response.data;
      }),
    );
  });
};

export const deleteTask = (id: number) => {
  return httpApi.delete(`/v1/task/delete/${id}`);
};
