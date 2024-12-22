import React, { useEffect, useState, useCallback } from 'react';
import { Avatar, Col, Row, Space, TablePaginationConfig } from 'antd';
import { Pagination, Tag, UsersTableRow, getUsersTableData } from 'api/users.api';
import { Table } from 'components/common/Table/Table';
import { ColumnsType } from 'antd/es/table';
import { Button } from 'components/common/buttons/Button/Button';
import { useTranslation } from 'react-i18next';
import { defineColorByPriority } from '@app/utils/utils';
import { notificationController } from 'controllers/notificationController';
import { Status } from '@app/components/profile/profileCard/profileFormNav/nav/payments/paymentHistory/Status/Status';
import { useMounted } from '@app/hooks/useMounted';
import { Checkbox, CheckboxGroup } from '@app/components/common/Checkbox/Checkbox';
import { Badge, Ribbon } from '@app/components/common/Badge/Badge';
import { DeleteOutlined, EditOutlined } from '@ant-design/icons';

const initialPagination: Pagination = {
  current: 1,
  pageSize: 5,
};

export const UsersTables: React.FC = () => {
  const [tableData, setTableData] = useState<{ data: UsersTableRow[]; pagination: Pagination; loading: boolean }>({
    data: [],
    pagination: initialPagination,
    loading: false,
  });
  const [interval, setInter] = useState<NodeJS.Timer>();

  const { t } = useTranslation();
  const { isMounted } = useMounted();

  const fetch = useCallback(
    (pagination: Pagination, loading: boolean) => {
      setTableData((tableData) => ({ ...tableData, loading: loading }));
      getUsersTableData(pagination).then((res) => {
        if (isMounted.current) {
          setTableData({ data: res.data, pagination: res.pagination, loading: false });
        }
      });
    },
    [isMounted],
  );

  useEffect(() => {
    fetch(tableData.pagination, true);
  }, [isMounted]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetch(tableData.pagination, false);
    }, 5000);
    return () => {
      clearInterval(intervalId);
    };
  }, [tableData.pagination]);

  // useEffect(() => {
  //   fetch(tableData.pagination, true);
  //   setInter(
  //     setInterval(() => {
  //       fetch(initialPagination, false);
  //     }, 5000),
  //   );
  // }, [fetch]);

  // const handleTableChange = (pagination: TablePaginationConfig) => {
  //   fetch(pagination, true);
  //   clearInterval(interval);
  //   setInter(
  //     setInterval(() => {
  //       fetch(pagination, false);
  //     }, 5000),
  //   );
  // };

  const handleDeleteRow = (rowId: number) => {
    // call delete user service
  };

  const handleEditRow = (rowId: number) => {
    // call delete user service
  };

  const columns: ColumnsType<UsersTableRow> = [
    {
      title: t('user.avatar'),
      dataIndex: 'avatar',
      key: 'avatar',
      render: (avatar: string) => <Avatar src={avatar} alt="Avatar" shape="circle" size={40} />,
    },
    {
      title: t('user.username'),
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: t('user.firstname'),
      dataIndex: 'first_name',
      key: 'first_name',
    },
    {
      title: t('user.lastname'),
      dataIndex: 'last_name',
      key: 'last_name',
    },
    {
      title: t('user.email'),
      dataIndex: 'email',
      key: 'email',
      // render: (text: string, record: { email: string; email_verified: boolean }) => {
      //   return <Badge status={record.email_verified ? 'success' : 'error'} text={record.email} />;
      // },
    },
    {
      title: t('user.phone'),
      dataIndex: 'phone',
      key: 'phone',
      // render: (text: string, record: { phone: string; phone_verified: boolean }) => {
      //   return <Badge status={record.phone_verified ? 'success' : 'error'} text={record.phone} />;
      // },
    },
    {
      title: t('user.active'),
      dataIndex: 'is_active',
      key: 'is_active',
      render: (text: string, record: { is_active: boolean }) => {
        return <Checkbox value="is_active" checked={record.is_active} disabled></Checkbox>;
      },
    },
    {
      title: t('user.superuser'),
      dataIndex: 'is_superuser',
      key: 'is_superuser',
      render: (text: string, record: { is_superuser: boolean }) => {
        return <Checkbox value="is_superuser" checked={record.is_superuser} disabled></Checkbox>;
      },
    },
    {
      title: t('tables.actions'),
      dataIndex: 'actions',
      key: 'actions',
      width: '15%',
      render: (text: string, record: { username: string; id: number }) => {
        return (
          <Space key={`${record.id}_actions`}>
            <Button
              type="primary"
              shape="circle"
              key="edit-button"
              size="small"
              onClick={() => handleEditRow(record.id)}
              icon={<EditOutlined />}
            ></Button>
            <Button
              type="primary"
              danger
              shape="circle"
              key="delete-button"
              size="small"
              onClick={() => handleDeleteRow(record.id)}
              icon={<DeleteOutlined />}
            ></Button>
          </Space>
        );
      },
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={tableData.data.map((item) => ({ ...item, key: item.id }))}
      pagination={tableData.pagination}
      loading={tableData.loading}
      // onChange={handleTableChange}
      scroll={{ x: 800 }}
      bordered
    />
  );
};
