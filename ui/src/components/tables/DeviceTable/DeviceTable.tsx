import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Avatar, Col, Row, Space, TablePaginationConfig, message } from 'antd';
import { Pagination, addDevice, DeviceTableRow, getDeviceTableData, deleteDevice } from '@app/api/device.api';
import { Table } from 'components/common/Table/Table';
import { ColumnsType } from 'antd/es/table';
import { Button } from 'components/common/buttons/Button/Button';
// import { Modal, InfoModal, SuccessModal, WarningModal, ErrorModal } from '@app/components/common/Modal/Modal';
import { useTranslation } from 'react-i18next';
import { useMounted } from '@app/hooks/useMounted';
import { Input, List, Tooltip  } from 'antd';
import type { InputRef } from 'antd';
import { DeleteOutlined, SettingOutlined, RightOutlined } from '@ant-design/icons';
import { readToken } from '@app/services/localStorage.service';
import * as mqtt from 'mqtt';
import InfiniteScroll from 'react-infinite-scroll-component';
import { notificationController } from '@app/controllers/notificationController';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { Checkbox, Form, Modal } from 'antd';
import TextArea from 'antd/lib/input/TextArea';

const initialPagination: Pagination = {
  current: 1,
  pageSize: 5,
};

export const DeviceTable: React.FC = () => {
  const [tableData, setTableData] = useState<{ data: DeviceTableRow[]; pagination: Pagination; loading: boolean }>({
    data: [],
    pagination: initialPagination,
    loading: false,
  });

  const token = process.env.REACT_APP_DEVICE_COMMAND_TOKEN;

  const [openAddDeviceModal, setOpenAddDeviceModal] = useState<boolean>(false);
  const [selectedDevice, setSelectedDevice] = useState<DeviceTableRow>();
  const [interval, setInter] = useState<NodeJS.Timer>();

  // const [socketUrl, setSocketUrl] = useState(
  //   `wss://${process.env.REACT_APP_BE}/ws/device/command/${readToken()}/${token}`,
  // );
  // const [messageHistory, setMessageHistory] = useState<string[]>([]);
  // const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const { t } = useTranslation();
  const { isMounted } = useMounted();
  const [form] = Form.useForm();

  // const bottomMessageRef = useRef<null | HTMLDivElement>(null);
  // const ContainerHeight = 400;
  // const connectionStatus = {
  //   [ReadyState.CONNECTING]: 'Connecting',
  //   [ReadyState.OPEN]: 'Open',
  //   [ReadyState.CLOSING]: 'Closing',
  //   [ReadyState.CLOSED]: 'Closed',
  //   [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  // }[readyState];

  const fetch = useCallback(
    (pagination: Pagination, loading: boolean) => {
      setTableData((tableData) => ({ ...tableData, loading: loading }));
      getDeviceTableData(pagination).then((res) => {
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

  const handleTableChange = (pagination: TablePaginationConfig) => {
    fetch(pagination, true);
    clearInterval(interval);
    setInter(
      setInterval(() => {
        fetch(pagination, false);
      }, 5000),
    );
  };

  const onSubmitForm = () => {
    form.validateFields().then((values) => {
      form.resetFields();
      addDevice(values).then((response) => {
        notificationController.success({ message: `${response['name']} added` });
        fetch(tableData.pagination, true);
      });
      setOpenAddDeviceModal(false);
    });
  };

  const handleDelete = (device_id: string) => {
    deleteDevice(device_id).then((response) => {
      notificationController.success({ message: `${response['name']} removed` });
      fetch(tableData.pagination, true);
    });
  };

  const columns: ColumnsType<DeviceTableRow> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: { name: string; id: number }) => {
        return <a href={`services?device_id=${record.id}`}>{record.name}</a>;
      },
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Owner',
      dataIndex: 'owner',
      key: 'owner',
    },
    // {
    //   title: 'Status',
    //   dataIndex: 'status',
    //   key: 'device_status',
    //   render: (text: string, record: { enable: boolean }) => {
    //     return record.enable ? 'Enable' : 'Disabled';
    //   },
    // },
    {
      title: 'Actions',
      key: 'file_actions',
      render: (record) => {
        return (
          <Space key={`${record.device_id}_actions`}>
            <Tooltip title="Setting">
              <Button 
                type="primary"
                shape="circle"
                href={`details?id=${record.id}`}
                key="delete-button"
                size="small"
                icon={<SettingOutlined />}
              ></Button>
            </Tooltip>
            <Tooltip title="Delete">
              <Button
                type="primary"
                danger
                shape="circle"
                key="delete-button"
                size="small"
                onClick={() => handleDelete(record.id)}
                icon={<DeleteOutlined />}
              ></Button>
            </Tooltip>
          </Space>
        );
      },
    },
  ];

  return (
    <>
      <Space>
        <Button onClick={() => setOpenAddDeviceModal(true)} size="small" type="primary" style={{ marginBottom: 16 }}>
          Add Device
        </Button>
        <Button size="small" type="primary" style={{ marginBottom: 16 }}>
          Scan
        </Button>
      </Space>

      <Table
        key="device_table"
        columns={columns}
        dataSource={tableData.data.map((item) => ({ ...item, key: item.id }))}
        pagination={tableData.pagination}
        loading={tableData.loading}
        onChange={handleTableChange}
        scroll={{ x: 800 }}
        size="small"
        bordered
      />

      <Modal
        title="Add Device"
        open={openAddDeviceModal}
        onOk={onSubmitForm}
        onCancel={() => setOpenAddDeviceModal(false)}
      >
        <Form
          name="basic"
          form={form}
          labelCol={{ span: 6 }}
          autoComplete="off"
          initialValues={{ enable: false, description: '' }}
        >
          <Form.Item label="Device Name" name="name" rules={[{ required: true, message: 'Please input device name' }]}>
            <Input />
          </Form.Item>

          <Form.Item label="Description" name="description">
            <TextArea />
          </Form.Item>

          <Form.Item name="enable" valuePropName="checked" wrapperCol={{ offset: 6, span: 16 }}>
            <Checkbox>Enable</Checkbox>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};
