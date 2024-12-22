import React, { useState, useEffect, useCallback } from 'react';
import { Popconfirm, Form, TablePaginationConfig, Space, notification } from 'antd';
import { EyeTwoTone, EyeInvisibleOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { ColumnsType } from 'antd/es/table';
import { Table } from 'components/common/Table/Table';
import { getDeviceTokenData, deleteToken, DeviceTokenTableRow, Pagination } from 'api/device-token.api';
import { EditableCell } from './EditableCell';
import { Button } from 'components/common/buttons/Button/Button';
import { InputPassword } from '@app/components/common/inputs/InputPassword/InputPassword';
import { useTranslation } from 'react-i18next';
import { useMounted } from '@app/hooks/useMounted';
import { notificationController } from '@app/controllers/notificationController';

const initialPagination: Pagination = {
  current: 1,
  pageSize: 5,
};

export const DeviceTokenTable: React.FC = () => {
  const [form] = Form.useForm();
  const [tableData, setTableData] = useState<{ data: DeviceTokenTableRow[]; pagination: Pagination; loading: boolean }>(
    {
      data: [],
      pagination: initialPagination,
      loading: false,
    },
  );
  const [editingKey, setEditingKey] = useState(0);
  const { t } = useTranslation();
  const { isMounted } = useMounted();
  const [interval, setInter] = useState<NodeJS.Timer>();

  const fetch = useCallback(
    (pagination: Pagination, loading: boolean) => {
      setTableData((tableData) => ({ ...tableData, loading: loading }));
      getDeviceTokenData(pagination).then((res) => {
        if (isMounted.current) {
          setTableData({ data: res.data, pagination: res.pagination, loading: false });
        }
      });
    },
    [isMounted],
  );

  useEffect(() => {
    fetch(initialPagination, true);
    setInter(
      setInterval(() => {
        fetch(initialPagination, false);
      }, 5000),
    );
  }, [fetch]);

  const handleTableChange = (pagination: TablePaginationConfig) => {
    fetch(pagination, true);
    clearInterval(interval);
    setInter(
      setInterval(() => {
        fetch(pagination, false);
      }, 5000),
    );
  };

  const handleEditRow = (id: number) => {
    console.log(id);
  };

  const handleDeleteRow = (rowId: number) => {
    deleteToken(rowId).then((res) => {
      notificationController.success({ message: `${res.data['token']} removed` });
      fetch(tableData.pagination, true);
    });
  };

  const columns: ColumnsType<DeviceTokenTableRow> = [
    {
      title: 'ID',
      width: '5%',
      key: 'id',
      dataIndex: 'id',
    },
    {
      title: 'Token',
      width: '20%',
      key: 'token',
      dataIndex: 'token',
      render: (text: string, record: DeviceTokenTableRow) => {
        return (
          <InputPassword
            size="small"
            value={record.token}
            iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
          />
        );
      },
    },
    {
      title: 'Device ID',
      dataIndex: 'device_id',
      key: 'device_id',
    },
    {
      title: 'Description',
      key: 'description',
      dataIndex: 'description',
    },
    {
      title: t('tables.actions'),
      dataIndex: 'actions',
      key: 'action',
      width: '15%',
      render: (text: string, record: DeviceTokenTableRow) => {
        return (
          <Space key={`${record.id}_actions`}>
            <Button
              type="primary"
              shape="circle"
              size="small"
              onClick={() => handleEditRow(record.id)}
              icon={<EditOutlined />}
            ></Button>
            <Button
              type="primary"
              danger
              shape="circle"
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
    <Form form={form} component={false}>
      <Table
        bordered
        dataSource={tableData.data}
        columns={columns}
        pagination={tableData.pagination}
        onChange={handleTableChange}
        loading={tableData.loading}
        scroll={{ x: 800 }}
      />
    </Form>
  );
};
