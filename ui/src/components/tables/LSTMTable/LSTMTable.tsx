import React, { useEffect, useState, useCallback } from 'react';
import { Avatar, Col, Row, Space, TablePaginationConfig, message } from 'antd';
import { Pagination, Tag, LSTMTableRow, getLSTMTableData } from '@app/api/lstm.api';
import { deleteTask } from '@app/api/task.api';
import { Table } from 'components/common/Table/Table';
import { ColumnsType } from 'antd/es/table';
import { Button } from 'components/common/buttons/Button/Button';
import { useTranslation } from 'react-i18next';
import { useMounted } from '@app/hooks/useMounted';
import { DeleteOutlined } from '@ant-design/icons';
import { readToken } from '@app/services/localStorage.service';
import { format } from 'date-fns';

const initialPagination: Pagination = {
  current: 1,
  pageSize: 5,
};

export const LSTMTable: React.FC = () => {
  const [tableData, setTableData] = useState<{ data: LSTMTableRow[]; pagination: Pagination; loading: boolean }>({
    data: [],
    pagination: initialPagination,
    loading: false,
  });
  const { t } = useTranslation();
  const { isMounted } = useMounted();
  const [interval, setInter] = useState<NodeJS.Timer>();

  const fetch = useCallback(
    (pagination: Pagination, loading: boolean) => {
      setTableData((tableData) => ({ ...tableData, loading: loading }));
      getLSTMTableData(pagination).then((res) => {
        if (isMounted.current) {
          setTableData({ data: res.data, pagination: res.pagination, loading: loading });
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
      }, 2000),
    );
  }, [fetch]);

  const handleTableChange = (pagination: TablePaginationConfig) => {
    fetch(pagination, true);
    clearInterval(interval);
    setInter(
      setInterval(() => {
        fetch(pagination, false);
      }, 2000),
    );
  };

  const handleDelete = (id: number) => {
    deleteTask(id).then((res) => {
      message.success(`${res.data['name']} removed`);
      fetch(tableData.pagination, false);
    });
  };

  const columns: ColumnsType<LSTMTableRow> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Log',
      dataIndex: 'ramq_queue',
      key: 'ramq_queue',
      render: (id: number, record: { ramq_queue: string }) => {
        return record.ramq_queue.split('|').map((value, index) => {
          return (
            <>
              <a key={index} href={'/apps/redis-message?queue=' + value}>
                {value}
              </a>
              <br />
            </>
          );
        });
      },
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: 'Output',
      dataIndex: 'output',
      key: 'output',
      render: (id: number, record: { output: string }) => {
        return (
          <a
            key={id}
            href={`${process.env.REACT_APP_API_URL}/v1/lstm/${record.output}/download?token=${readToken()}`}
            target="_blank"
            rel="noreferrer"
          >
            {record.output}
          </a>
        );
      },
    },
    {
      title: 'Created Date',
      dataIndex: 'created_date',
      key: 'created_date',
      render: (id: number, record: { created_date: string }) => {
        const date = new Date(record.created_date);
        date.setTime(date.getTime() + 7 * 60 * 60 * 1000);
        return <p>{date.toLocaleString()}</p>;
      },
    },
    {
      key: 'file_actions',
      render: (id: number, record: { id: number }) => {
        return (
          <Space key={`${record.id}_actions`}>
            <Button
              type="primary"
              danger
              shape="circle"
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
    <Table
      key="file_table"
      columns={columns}
      dataSource={tableData.data}
      pagination={tableData.pagination}
      loading={tableData.loading}
      onChange={handleTableChange}
      scroll={{ x: 800 }}
      bordered
    />
  );
};
