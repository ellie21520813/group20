import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Avatar, Col, Row, Space, TablePaginationConfig, message } from 'antd';
import {
  Pagination,
  addDeviceConfigs,
  DeviceConfigRow,
  getDeviceConfig,
  deleteDeviceConfig,
} from '@app/api/device.api';
import { Table } from 'components/common/Table/Table';
import { ColumnsType } from 'antd/es/table';
import { Button } from 'components/common/buttons/Button/Button';
import { Modal, InfoModal, SuccessModal, WarningModal, ErrorModal } from '@app/components/common/Modal/Modal';
import { useTranslation } from 'react-i18next';
import { useMounted } from '@app/hooks/useMounted';
import { Form, Input, Card } from 'antd';
import { DeleteOutlined, MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import { notificationController } from '@app/controllers/notificationController';

const initialPagination: Pagination = {
  current: 1,
  pageSize: 5,
};

export const DeviceConfigTable: React.FC<{ device_id: string }> = ({ device_id }) => {
  const [tableData, setTableData] = useState<{ data: DeviceConfigRow[]; pagination: Pagination; loading: boolean }>({
    data: [],
    pagination: initialPagination,
    loading: false,
  });
  const { t } = useTranslation();
  const { isMounted } = useMounted();
  const [form] = Form.useForm();

  const token = process.env.REACT_APP_DEVICE_COMMAND_TOKEN;

  const [interval, setInter] = useState<NodeJS.Timer>();
  const [config, setConfig] = useState();
  const [openAddConfigModal, setOpenAddConfigModal] = useState<boolean>(false);

  const fetch = (device_id: string, pagination: Pagination, loading: boolean) => {
    if (device_id != '') {
      setTableData((tableData) => ({ ...tableData, loading: loading }));
      getDeviceConfig(device_id, pagination).then((res) => {
        if (isMounted.current) {
          setTableData({ data: res.data, pagination: res.pagination, loading: false });
        }
      });
    }
  };

  useEffect(() => {
    fetch(device_id, tableData.pagination, true);
  }, [isMounted, device_id]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetch(device_id, tableData.pagination, false);
    }, 5000);
    return () => {
      clearInterval(intervalId);
    };
  }, [tableData.pagination, device_id]);

  const handleTableChange = (pagination: TablePaginationConfig) => {
    fetch(device_id, pagination, true);
    clearInterval(interval);
    setInter(
      setInterval(() => {
        fetch(device_id, pagination, false);
      }, 5000),
    );
  };

  const addConfig = () => {
    setOpenAddConfigModal(true);
  };

  const onFinish = () => {
    form.validateFields().then((values) => {
      form.resetFields();
      if (values.configs != undefined) {
        const res = {
          device_id: parseInt(device_id),
          ...values,
        };
        addDeviceConfigs(res).then((response) => {
          response.configs.forEach((config: { key: string; value: string }) => {
            notificationController.success({ message: `${config['key']}:${config['value']} added` });
            fetch(device_id, tableData.pagination, true);
          });
        });
      }
    });
    setOpenAddConfigModal(false);
  };

  const handleDelete = (id: number) => {
    deleteDeviceConfig(id).then((response) => {
      notificationController.success({ message: `${response['key']} removed` });
      fetch(device_id, tableData.pagination, true);
    });
  };

  const columns: ColumnsType<DeviceConfigRow> = [
    {
      title: 'Key',
      dataIndex: 'key',
      key: 'key',
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 100,
      fixed: 'right',
      render: (record) => {
        return (
          <Space key={`${record.device_id}_actions`}>
            <Button
              type="primary"
              danger
              shape="circle"
              key="delete-button"
              size="small"
              onClick={() => handleDelete(record.id)}
              icon={<DeleteOutlined />}
            ></Button>
          </Space>
        );
      },
    },
  ];

  return (
    <>
      <Button onClick={addConfig} size="small" type="primary" style={{ marginBottom: 16 }}>
        Add Config
      </Button>
      <Table
        key="device_config_table"
        columns={columns}
        dataSource={tableData.data.map((item) => ({ ...item }))}
        pagination={tableData.pagination}
        loading={tableData.loading}
        onChange={handleTableChange}
        size="small"
        bordered
      />

      <Modal
        title="Add Config"
        open={openAddConfigModal}
        size="medium"
        onOk={onFinish}
        onCancel={() => {
          form.resetFields();
          setOpenAddConfigModal(false);
        }}
      >
        <Form form={form} name="dynamic_form_nest_item" autoComplete="off">
          <Form.List name="configs">
            {(fields, { add, remove }) => (
              <>
                {fields.map(({ key, name, ...restField }) => (
                  <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                    <Form.Item {...restField} name={[name, 'key']} rules={[{ required: true, message: 'Missing key' }]}>
                      <Input placeholder="Key" />
                    </Form.Item>
                    <Form.Item
                      {...restField}
                      name={[name, 'value']}
                      rules={[{ required: true, message: 'Missing value' }]}
                    >
                      <Input placeholder="Value" />
                    </Form.Item>
                    <MinusCircleOutlined onClick={() => remove(name)} />
                  </Space>
                ))}
                <Form.Item>
                  <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                    Add config
                  </Button>
                </Form.Item>
              </>
            )}
          </Form.List>
        </Form>
      </Modal>
    </>
  );
};
