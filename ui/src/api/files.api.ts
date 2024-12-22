import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}

export interface FileTableRow {
  id: number;
  file_id: string;
  name: string;
  size: number;
  ext: string;
  type: string;
  local_url: string;
  is_public: boolean;
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

export interface FileTableData {
  data: FileTableRow[];
  pagination: Pagination;
}

export const getFileTableData = (pagination: Pagination): Promise<FileTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post('/v1/file/all', { ...pagination }).then((response) => {
        return response.data;
      }),
    );
  });
};

export const deleteFile = (file_id: string) => {
  return httpApi.delete(`http://localhost/api/v1/file/${file_id}`);
};
