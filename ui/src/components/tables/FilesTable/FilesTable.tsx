import React, { useEffect, useState, useCallback } from 'react';
import { Avatar, Col, Row, Space, TablePaginationConfig, message } from 'antd';
import { Pagination, Tag, FileTableRow, getFileTableData } from 'api/files.api';
import { Table } from 'components/common/Table/Table';
import { ColumnsType } from 'antd/es/table';
import { Button } from 'components/common/buttons/Button/Button';
import { useTranslation } from 'react-i18next';
import { useMounted } from '@app/hooks/useMounted';
import { Checkbox, CheckboxGroup } from '@app/components/common/Checkbox/Checkbox';
import { httpApi } from '@app/api/http.api';
import { readToken } from '@app/services/localStorage.service';
import { FileIcon, defaultStyles, DefaultExtensionType } from 'react-file-icon';
import { DeleteOutlined, EditOutlined, EyeOutlined, DownloadOutlined } from '@ant-design/icons';
import { notificationController } from '@app/controllers/notificationController';

const initialPagination: Pagination = {
  current: 1,
  pageSize: 5,
};

export const FilesTable: React.FC = () => {
  const [tableData, setTableData] = useState<{ data: FileTableRow[]; pagination: Pagination; loading: boolean }>({
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
      getFileTableData(pagination).then((res) => {
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

  const handleDelete = (file_id: string) => {
    httpApi.delete(`/v1/file/${file_id}`).then((response) => {
      const file_info = response.data;
      notificationController.success({ message: `${file_info['name']} removed` });
      fetch(tableData.pagination, true);
    });
  };

  const columns: ColumnsType<FileTableRow> = [
    {
      title: '#',
      dataIndex: 'file_icon',
      key: 'file_icon',
      render: (text: string, record: { file_id: string; ext: string }) => {
        const extension = record.ext.replace('.', '');
        return (
          <FileIcon key={record.file_id} extension={extension} {...defaultStyles[extension as DefaultExtensionType]} />
        );
      },
    },
    {
      title: t('file.name'),
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: { file_id: string; name: string; ext: string }) => {
        return (
          <a
            href={`${process.env.REACT_APP_API_URL}/v1/file/${record.file_id}${record.ext}?token=${readToken()}`}
            target="_blank"
            rel="noreferrer"
          >
            {record.name}
          </a>
        );
      },
    },
    {
      title: t('file.id'),
      dataIndex: 'file_id',
      key: 'file_id',
    },
    {
      title: t('file.size'),
      dataIndex: 'size',
      key: 'size',
    },
    {
      title: t('file.ext'),
      dataIndex: 'ext',
      key: 'ext',
    },
    {
      title: t('file.type'),
      dataIndex: 'type',
      key: 'type',
    },
    {
      title: t('file.isPublic'),
      dataIndex: 'is_public',
      key: 'is_public',
      render: (text: string, record: { file_id: string; is_public: boolean }) => {
        return <Checkbox key={record.file_id} value="is_public" checked={record.is_public} disabled></Checkbox>;
      },
    },
    {
      title: t('file.owner'),
      dataIndex: 'created_by',
      key: 'created_by',
    },
    {
      title: t('tables.actions'),
      key: 'file_actions',
      width: '15%',
      render: (text: string, record: { file_id: string; ext: string }) => {
        return (
          <Space>
            <Button
              type="primary"
              shape="circle"
              size="small"
              href={`${process.env.REACT_APP_API_URL}/v1/file/${record.file_id}${record.ext}?token=${readToken()}`}
              target="_blank"
              icon={<EyeOutlined />}
            ></Button>
            <Button
              type="primary"
              shape="circle"
              size="small"
              href={`${process.env.REACT_APP_API_URL}/v1/file/${record.file_id}${
                record.ext
              }/download?token=${readToken()}`}
              target="_blank"
              icon={<DownloadOutlined />}
            ></Button>
            <Button
              type="primary"
              danger
              shape="circle"
              size="small"
              onClick={() => handleDelete(record.file_id)}
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
      size='small'
      columns={columns}
      dataSource={tableData.data.map((item) => ({ ...item, key: item.file_id }))}
      pagination={tableData.pagination}
      loading={tableData.loading}
      onChange={handleTableChange}
      scroll={{ x: 800 }}
      bordered
    />
  );
};
