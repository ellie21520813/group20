import React, { useEffect, useState, useCallback } from 'react';
import { Avatar, Col, Row, Space, TablePaginationConfig, message } from 'antd';
import {
  Pagination,
  Tag,
  DeviceDiscoverTableRow,
  DiscoverdDeviceTableData,
  getDiscoverdDeviceTableData,
  deleteDiscoveredDevice,
} from '@app/api/device-discover.api';
import { Table } from 'components/common/Table/Table';
import { ColumnsType } from 'antd/es/table';
import { Button } from 'components/common/buttons/Button/Button';
import { Modal, InfoModal, SuccessModal, WarningModal, ErrorModal } from '@app/components/common/Modal/Modal';
import { useTranslation } from 'react-i18next';
import { useMounted } from '@app/hooks/useMounted';
import { DeleteOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { readToken } from '@app/services/localStorage.service';
import * as mqtt from 'mqtt';

const initialPagination: Pagination = {
  current: 1,
  pageSize: 5,
};

export const DiscoverTable: React.FC = () => {
  const [tableData, setTableData] = useState<{
    data: DeviceDiscoverTableRow[];
    pagination: Pagination;
    loading: boolean;
  }>({
    data: [],
    pagination: initialPagination,
    loading: false,
  });
  const [isDeviceInfoModalOpen, setIsDeviceInfoModelOpen] = useState<boolean>(false);
  const [selectedDevice, setSelectedDevice] = useState<DeviceDiscoverTableRow>();
  const [interval, setInter] = useState<NodeJS.Timer>();

  const { t } = useTranslation();
  const { isMounted } = useMounted();

  const fetch = useCallback(
    (pagination: Pagination, loading: boolean) => {
      setTableData((tableData) => ({ ...tableData, loading: loading }));
      getDiscoverdDeviceTableData(pagination).then((res) => {
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

  const handleRefresh = () => {
    fetch(tableData.pagination, true);
  };

  const handleDelete = (device_id: string) => {
    deleteDiscoveredDevice(device_id).then((response) => {
      message.success(`${response['name']} removed`);
      fetch(tableData.pagination, true);
    });
  };

  const deviceInfo = (device: DeviceDiscoverTableRow) => {
    setSelectedDevice(device);
    setIsDeviceInfoModelOpen(true);
  };

  const columns: ColumnsType<DeviceDiscoverTableRow> = [
    {
      title: 'ID',
      dataIndex: 'device_id',
      key: 'device_id',
    },
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'device_id',
    },
    {
      title: 'Hostname',
      dataIndex: 'hostname',
      key: 'device_hosname',
    },
    {
      title: 'IP',
      dataIndex: 'ip',
      key: 'device_ip',
    },
    {
      title: 'Last scan',
      dataIndex: 'updated_date',
      key: 'updated_date',
      render: (text: string, record: { updated_date: string }) => {
        const date = new Date(record.updated_date);
        date.setTime(date.getTime() + 7 * 60 * 60 * 1000);
        return <p>{date.toLocaleString()}</p>;
      },
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'device_status',
    },
    {
      title: <Button onClick={() => handleRefresh()}>Scan</Button>,
      key: 'file_actions',
      render: (record) => {
        return (
          <Space key={`${record.device_id}_actions`}>
            <Button
              type="primary"
              danger
              shape="circle"
              key="delete-button"
              size="small"
              onClick={() => handleDelete(record.device_id)}
              icon={<DeleteOutlined />}
            ></Button>
            <Button
              type="primary"
              shape="circle"
              key="info-button"
              size="small"
              onClick={() => deviceInfo(record)}
              icon={<InfoCircleOutlined />}
            ></Button>
          </Space>
        );
      },
    },
  ];

  return (
    <>
      <Table
        key="discovered_device_table"
        columns={columns}
        dataSource={tableData.data}
        pagination={tableData.pagination}
        loading={tableData.loading}
        onChange={handleTableChange}
        scroll={{ x: 800 }}
        bordered
      />
      <Modal
        title={selectedDevice?.name}
        open={isDeviceInfoModalOpen}
        onOk={() => setIsDeviceInfoModelOpen(false)}
        onCancel={() => setIsDeviceInfoModelOpen(false)}
      >
        <p>IP: {selectedDevice?.ip}</p>
        <p>Hostname: {selectedDevice?.hostname}</p>
      </Modal>
    </>
  );
};
