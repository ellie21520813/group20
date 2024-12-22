import { Priority } from '../constants/enums/priorities';
import { httpApi } from '@app/api/http.api';

export interface Tag {
  value: string;
  priority: Priority;
}

export interface UsersTableRow {
  id: number;
  first_name: string;
  last_name: string;
  username: string;
  avatar: string;
  email: string;
  email_verified: boolean;
  phone: string;
  phone_verified: boolean;
  is_active: boolean;
  is_superuser: boolean;
  tags?: Tag[];
}

export interface Pagination {
  current?: number;
  pageSize?: number;
  total?: number;
}

export interface UsersTableData {
  data: UsersTableRow[];
  pagination: Pagination;
}

export const getUsersTableData = (pagination: Pagination): Promise<UsersTableData> => {
  return new Promise((res) => {
    res(
      httpApi.post('/v1/user/all', { ...pagination }).then((response) => {
        return response.data;
      }),
    );
  });
};
